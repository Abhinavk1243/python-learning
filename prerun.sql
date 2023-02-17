drop table if exists current_elig_1;
CREATE LOCAL TEMP TABLE current_elig_1 ON COMMIT PRESERVE ROWS AS
SELECT DISTINCT 
       reporting_end_period,
       reporting_period_type,
       reportgroupid,
       customerid,
       guid,
       hashkey,
       BIEffectiveDate,
       BIEndDate
FROM (SELECT reporting_end_period,
             reporting_period_type,
             x.reportgroupid,
             CASE WHEN LENGTH(x.customerid) > 4 THEN x.customerid ELSE NULL END AS customerid,
             x.guid::varchar(100),
             x.hashkey::varchar(100),
             x.BIEffectiveDate::Date,
             x.BIEndDate::Date
      FROM bi_reporting.eliggroupingmembers x
      JOIN (SELECT DISTINCT aa.reportgroupid 
            FROM bi_reporting.eliggroupingmembers aa
            JOIN sharecare.sc_employer_membership bb 
            ON (aa.guid::varchar(100) = bb.guid::varchar(100) AND bb.deleted_flg IS NULL AND (bb.test_account = 'false' OR bb.test_account IS NULL))) rep
      ON (x.reportgroupid = rep.reportgroupid)
      JOIN run_params rp                      
      ON (rp.entity = x.reportgroupid AND rp.reporting_end_period::date BETWEEN x.BIEffectiveDate::Date AND x.BIEndDate::Date)
      JOIN (SELECT DISTINCT reportgroupid FROM bi_reporting.eliggroupingrules WHERE isactive = 1) dd 
      ON (rep.reportgroupid = dd.reportgroupid)) a;

select analyze_statistics('current_elig_1');


drop table if exists current_elig_2;
create local temp table current_elig_2 on commit preserve rows as
select distinct el.*
from current_elig_1 el
join (select guid::varchar(100),customerid,dob,bieffectivefromdate,bieffectivetodate,eligibilitystartdate,eligibilityenddate from bi_reporting.eligibility_history where testuser = 'N') eh
on (el.guid::varchar(100)=eh.guid::varchar(100) and case when nullif(el.customerid,'') is null then eh.customerid else el.customerid end=eh.customerid)
where age_in_years(el.reporting_end_period::date,eh.dob)>=18 
AND el.reporting_end_period::date BETWEEN eh.BIEFFECTIVEFROMDATE::date AND eh.BIEFFECTIVETODATE::date
AND el.reporting_end_period::date BETWEEN eh.ELIGIBILITYSTARTDATE::date AND eh.ELIGIBILITYENDDATE::date;

select analyze_statistics('current_elig_2');

drop table if exists current_elig_3;
create local temp table current_elig_3 on commit preserve rows as
select distinct el.reportgroupid,min_tests,count(distinct cc.secure_id) as tests
from current_elig_2 el
join ent_wh.registrants reg
        on (el.guid::varchar(100)=reg.guid::varchar(100)
                and case when nullif(el.customerid,'') is null then reg.customerid else el.customerid end=reg.customerid)
left join sc_kpi.thresholds_test_completes tc on (el.reportgroupid=tc.reportgroupid)
left join sharecare.sc_assessment_history_ratm cc
        on (reg.secure_id=cc.secure_id                      
                and to_char(cc.creation_date,'yyyy-mm') >= to_char(add_months(sysdate,-18),'yyyy-mm')
                and to_char(cc.creation_date,'yyyy-mm') <= to_char(add_months(sysdate,-1),'yyyy-mm'))
group by 1,2;


drop table if exists current_elig;
create local temp table current_elig on commit preserve rows as
select distinct el.*
from current_elig_2 el
join current_elig_3 el2 on (el.reportgroupid=el2.reportgroupid)
where (tests>=50 and min_tests is null) or (tests>=min_tests);

select analyze_statistics('current_elig');


drop table if exists calendar_table;
create local temp table calendar_table on commit preserve rows as
select
distinct
trunc(r.reporting_end_period,'mm')::date as b_p,
r.reporting_end_period as e_p
from dwimp.dwimp_date m
join (select distinct reporting_end_period from run_params) r on m.month_id=to_char(r.reporting_end_period,'yyyymm');


delete from sc_kpi.qbr_incentive_allelig_curryear_xwalk
where incent_elig_month = (select max(to_char(reporting_end_period,'yyyy-mm') ) from run_params );

insert into sc_kpi.qbr_incentive_allelig_curryear_xwalk
select distinct
        nullif(b.employerid,'')
        , em.collectionid
        , b.guid
        , b.customerid
        , em.program_id
        , b.month_id as incent_elig_month
    from
        (
        select
            e.guid
            , e.employerid
            , e.customerid
            , to_char(ct.e_p,'yyyy-mm') as month_id
            , greatest(e.eligibilitystartdate::timestamp,e.bieffectivefromdate,timestampadd(month,-1*month(ct.e_p),ct.e_p)::date+1)::date as elig_eff
            , least(e.eligibilityenddate::timestamp,e.bieffectivetodate,ct.e_p)::date as elig_end
        from bi_reporting.eligibility_history e
            cross join calendar_table ct
        where greatest(e.eligibilitystartdate::timestamp,e.bieffectivefromdate)::date <= ct.e_p
            and least(e.eligibilityenddate::timestamp,e.bieffectivetodate)::date >= timestampadd(month,-1*month(ct.e_p),ct.e_p)::date+1
            and e.testuser = 'N'            
        ) b
        inner join bi_reporting.incentive_elig_member em on b.customerid = em.customerid
            and b.guid::varchar(100) = em.guid::varchar(100)
            and em.incentive_elig_eff_date <= b.elig_end
            and em.incentive_elig_end_date >= b.elig_eff
    where b.elig_eff <= b.elig_end;
	

 
 
select analyze_statistics('sc_kpi.qbr_incentive_allelig_curryear_xwalk'); 


delete from sc_kpi.qbr_incentive_earned_allelig_curryear
where report_month = (select max(to_char(reporting_end_period,'yyyy-mm') ) from run_params );


insert into sc_kpi.qbr_incentive_earned_allelig_curryear
select distinct guid,client_id,report_month,reward_earned_date,reward_event_group_name,event_description
from 
	(
        select distinct c.guid,a.client_id,ct1.month_id report_month,reward_earned_date,reward_event_group_name,event_description,
		case 
			when to_char(a.reward_earned_date,'yyyy') = to_char(r.reporting_end_period,'yyyy') 
			and to_char(a.reward_earned_date,'yyyy-mm') <= ct1.month_id then 'Y' 
			else 'N 'end participation_month_flg
        from bi_reporting.incentive_earned_reporting_base a
        join
        (
            select distinct program_id, p.date_config_start_date, coalesce(p.date_config_end_date,'31Dec2999'::date) as date_config_end_date
            from sharecare.sc_incent_program p
            inner join calendar_table ct on p.date_config_start_date::Date <= ct.e_p::Date 
            and to_char(e_p,'yyyy') between to_char(p.date_config_start_date,'yyyy') and to_char(coalesce(p.date_config_end_date,'31Dec2999'),'yyyy') 
        ) p on a.program_id = p.program_id  
        join sharecare.sc_employer_membership c on a.secure_id = c.secure_id and a.client_id = c.customer and c.deleted_flg is null
        join sc_kpi.qbr_incentive_allelig_curryear_xwalk cex on cex.guid::int=c.guid::int and a.program_id=cex.program_id  and cex.customerid = c.customer 
		join (select distinct reporting_end_period from run_params ) r on cex.incent_elig_month >= to_char(trunc(r.reporting_end_period,'YYYY'),'yyyy-mm') 
		and cex.incent_elig_month<=to_char(r.reporting_end_period,'yyyy-mm')
        join 
		(  
			select distinct guid,customerid,ct.month_id elig_month,
            case 
				when to_char(greatest(eh.eligibilitystartdate::date,eh.bieffectivefromdate::date),'yyyy-mm') <= ct.month_id
				and to_char(least(eh.eligibilityenddate::date,eh.bieffectivetodate::date),'yyyy-mm') >=  to_char(trunc(r.reporting_end_period,'YYYY'),'yyyy-mm')
			then 'Y' ELSE 'N' END Elig_Flg
            from bi_reporting.eligibility_history eh
            cross join ( select to_char(e_p,'yyyy-mm') month_id from calendar_table ) ct    
			join (select distinct reporting_end_period from run_params ) r on ct.month_id=to_char(r.reporting_end_period,'yyyy-mm') 
            where testuser = 'N'
            order by 1,2,3
        )x on (c.guid::int = x.guid::int and c.customer = x.customerid and elig_flg = 'Y')
        cross join ( select to_char(e_p,'yyyy-mm') month_id  from calendar_table ) ct1      
	)a
	where participation_month_flg = 'Y'
	order by 1,2,3;
 
select analyze_statistics('sc_kpi.qbr_incentive_earned_allelig_curryear'); 
 
 


drop table if exists incent_top5_eventgroup;
create local temp table incent_top5_eventgroup on commit preserve rows as
select reportgroupid,report_month,reward_event_group_name,incent_earner,row_number() over(partition by reportgroupid,report_month order by incent_earner desc)event_group_rank
	from 
	(
        select reportgroupid,report_month,reward_event_group_name,count(distinct guid::int)incent_earner
        from 
		(
            select curr.reportgroupid,xw.guid::int,xw.client_id,xw.report_month,xw.reward_earned_date,nvl(xw.REWARD_EVENT_GROUP_NAME,'Non Group Activity')reward_event_group_name,xw.event_description
            from  sc_kpi.qbr_incentive_earned_allelig_curryear xw
            join  bi_reporting.eliggroupingmembers yy on xw.guid::int=yy.guid::int and case when yy.customerid is null then xw.client_id else yy.customerid end=xw.client_id
            join (select distinct reporting_end_period from run_params ) r on  to_char(yy.bienddate::date,'yyyy-mm') >= to_char(trunc(r.reporting_end_period,'yyyy'),'yyyy-mm')
            and to_char(yy.bieffectivedate::date,'yyyy-mm')<= to_char(r.reporting_end_period,'yyyy-mm')
            join (select distinct reportgroupid from current_elig) curr on (yy.reportgroupid=curr.reportgroupid)
            WHERE report_month=to_char(r.reporting_end_period,'yyyy-mm')
        ) x
        group by 1,2,3
    ) y;




drop table if exists incent_top5_eventdescription;
create local temp table incent_top5_eventdescription on commit preserve rows as
select reportgroupid,report_month,reward_event_group_name,event_description,incent_earner,row_number() over(partition by reportgroupid,report_month,reward_event_group_name order by incent_earner desc)event_desc_rank
	from 
	(
        select xx.reportgroupid,
		xx.report_month,xx.reward_event_group_name,xx.event_description,count(distinct xx.guid::int)incent_earner
        from 
		(
			select curr.reportgroupid,xw.guid::int,xw.client_id,xw.report_month,xw.reward_earned_date,nvl(xw.REWARD_EVENT_GROUP_NAME,'Non Group Activity')reward_event_group_name,xw.event_description
			from  sc_kpi.qbr_incentive_earned_allelig_curryear xw
			join bi_reporting.eliggroupingmembers yy on xw.guid::int=yy.guid::int and case when yy.customerid is null then xw.client_id else yy.customerid end=xw.client_id
			join (select distinct reporting_end_period from run_params ) r on to_char(yy.bienddate::date,'yyyy-mm') >= to_char(trunc(r.reporting_end_period,'yyyy'),'yyyy-mm')
			and to_char(yy.bieffectivedate::date,'yyyy-mm')<= to_char(r.reporting_end_period,'yyyy-mm')
			join (select distinct reportgroupid from current_elig) curr on (yy.reportgroupid=curr.reportgroupid)
			WHERE report_month=to_char(r.reporting_end_period,'yyyy-mm')
        ) xx
        join incent_top5_eventgroup yy on (xx.reportgroupid = yy.reportgroupid and xx.report_month = yy.report_month and xx.reward_event_group_name = yy.reward_event_group_name and yy.event_group_rank <= 5)
        group by 1,2,3,4
	) yy2;
 


