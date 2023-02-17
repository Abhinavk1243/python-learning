import json
import re
# f=open(f"qbr_json_final.json",)
str1="""
drop table if exists kpi_validation; CREATE LOCAL TEMP TABLE kpi_validation ON COMMIT PRESERVE ROWS AS
select b.*, (("(q4-q3)%" + "(q2-q3)%"+"(q2-q1)%")/3) as threshold from (
	select METRIC_ID,entity,q4,q3,q2,q1,month_ending_q4,month_ending_q3,month_ending_q2,month_ending_q1,
	abs((q4-q3)/q3) *100    "(q4-q3)%",
	abs((q3-q2)/q2) *100    "(q2-q3)%",
	abs((q2-q1)/q1) *100    "(q2-q1)%"
	
	from (
	
	with run_params_cte as (select distinct reporting_end_period  from run_params limit 1) 
	select  distinct
		
		a.entity,
		g.ReportGroupID,
		a.metric_id,
		a.reporting_end_period "month_ending_q4",
		b.reporting_end_period "month_ending_q3",
		c.reporting_end_period "month_ending_q2",
		d.reporting_end_period "month_ending_q1",
		sum(a.metric_value) q4,
		sum(b.metric_value) "q3",
		sum(c.metric_value)"q2",
		sum(d.metric_value)  "q1"
		from    
		(
			select  distinct ReportGroupName, ReportGroupID
			from    BI_REPORTING.EligGroupingMembers
			where   isactive=1
		) g
		join    sc_kpi.metrics_values a       on a.entity=g.ReportGroupid
		 full outer  join   sc_kpi.metrics_values b       on a.entity=b.entity and a.metric_id=b.metric_id and nvl(a.dims,'aaa') = nvl(b.dims, 'aaa')
		join run_params_cte as r on to_char(b.reporting_end_period,'yyyy-mm') = case when (ceil((to_number(to_char(r.reporting_end_period,'mm'))/3))-1)*3 = 0 
		then to_char(year(r.reporting_end_period)-1) || '-12'  
		else to_char(r.reporting_end_period,'yyyy') || '-' || trim(to_char((ceil((to_number(to_char(r.reporting_end_period,'mm'))/3))-1)*3,'09')) 
		end  
		 full outer join    sc_kpi.metrics_values c       on a.entity=c.entity and a.metric_id=c.metric_id and nvl(a.dims,'aaa') = nvl(c.dims, 'aaa')
		 and to_char(c.reporting_end_period,'yyyy-mm') = case when (ceil((to_number(to_char(r.reporting_end_period,'mm'))/3))-1)*3 = 0 
		then to_char(year(r.reporting_end_period)-1) || '-09' 
		when (ceil((to_number(to_char(r.reporting_end_period,'mm'))/3))-1)*3-3 = 0 
		then to_char(year(r.reporting_end_period)-1) || '-12'  
		else  to_char(r.reporting_end_period,'yyyy') || '-' || trim(to_char(((ceil((to_number(to_char(r.reporting_end_period,'mm'))/3))-1)*3-3),'09'))  end
		full outer join    sc_kpi.metrics_values d       on a.entity=d.entity and a.metric_id=d.metric_id and nvl(a.dims,'aaa') = nvl(d.dims, 'aaa')
		and to_char(d.reporting_end_period,'yyyy-mm') = case when (ceil((to_number(to_char(r.reporting_end_period,'mm'))/3))-1)*3 = 0 
		then to_char(year(r.reporting_end_period)-1) || '-06' 
		when (ceil((to_number(to_char(r.reporting_end_period,'mm'))/3))-1)*3-3 = 0 
		then to_char(year(r.reporting_end_period)-1) || '-09'  
		when (ceil((to_number(to_char(r.reporting_end_period,'mm'))/3))-1)*3-6 = 0 
		then to_char(year(r.reporting_end_period)-1) || '-12'  
		else  to_char(r.reporting_end_period,'yyyy') || '-' || trim(to_char(((ceil((to_number(to_char(r.reporting_end_period,'mm'))/3))-1)*3-6),'09'))  end
		Join sc_kpi.metrics_metadata m on  a.metric_id= m.metric_id and m.functional_area like 'qbr_%'
		where   to_char(a.reporting_end_period,'yyyy-mm') =   to_char(r.reporting_end_period,'yyyy-mm')
		 and b.metric_value is not null and b.metric_value <> 0 and d.metric_value <>0 and c.metric_value <> 0
	
		and a.metric_id::int not in (100002082,100002208) and a.entity not in ('8500001','8500002','8500003')
		group by 1,2,3,4,5,6,7
		order by 1,2,4
	
 ) a ) b
 where abs(q4-q3)::int >0  and abs(q3-q2)::int >0  and abs(q2-q1)::int >0 --and q3>1000 and q4 >1000 and q2>1000 and q1>1000
 and (q4-q3)::int >0  and q4>200 and q3>200 and q2 >200 and q1>200
 ;
 
 drop table if exists threshold;
CREATE LOCAL TEMP TABLE threshold ON COMMIT PRESERVE ROWS AS
 select metric_id,sum(threshold) /count(*) as avg_threshold from kpi_validation group by metric_id ;
 
 
drop table if exists validation_result;
create local temp table validation_result on commit preserve rows as
 select  month_ending_q4 month_ending_q2,month_ending_q3 month_ending_q1, v.metric_id ,entity ,q4 metric_value_Q2,q3 metric_value_Q1 ,"(q4-q3)%" validation_value ,threshold,t.avg_threshold,
 case
  when  "(q4-q3)%" <= (threshold+t.avg_threshold) then 'PASS'  
 else case when abs(validation_value-(threshold+t.avg_threshold))::int <=50  then 'PASS'  else 'fail'end end  result
 from   kpi_validation  v join threshold  t  on v.metric_id = t.metric_id ;
"""
list_dict=json.dumps({'query':str1})
# print(dict_2)
# data_query=[]
# metric_ids = []
# for dict in list_dict:
#     data_query.append(dict['data_query'])


# # for query in data_query:
#     query =dict['data_query']
#     txt = str(query)
#     p11= "metric_id\s=\s[0-9]{1,4}"
#     p12 = "metric_id=[0-9]{1,4}"
#     x1=re.findall(p11,txt)
#     y1=re.findall(p12,txt)
#     if x1:
#         p = "metric_id\s=\s"
#         x = re.sub(p, "metric_id=10000", txt)
#     if y1:
#         p1 = "metric_id="
#         y=re.sub(p1, "metric_id=10000", txt)
    
    
#     # print(x)
    
#     if x1:
#         # metric_ids=metric_ids + [x]
#         dict['data_query']=x
#     if y1:
#         # metric_ids=metric_ids+[y]
#         dict['data_query']=y
    
#     metric_ids.append(dict)
#     # print(dict)
    
with open("qbr_json_final_new.json", "w") as outfile:
    json.dump(list_dict, outfile)

# print(len(metric_ids))

# print(len(list_dict))