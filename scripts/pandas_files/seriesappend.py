import os 
from configparser import ConfigParser
import vertica_python
import pandas as pd
import argparse
import numpy as np
import sys
import logging as lg
from datetime import datetime,date,timedelta
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email import encoders

from jinja2 import Environment, FileSystemLoader


def logger():
    logger = lg.getLogger(__name__)
    logger.setLevel(lg.INFO)
    formatter = lg.Formatter('%(asctime)s : %(name)s : %(filename)s : %(levelname)s : %(funcName)s :%(lineno)d : %(message)s ')
    file_handler =lg.FileHandler("logs.log")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    consoleHandler = lg.StreamHandler()
    consoleHandler.setFormatter(formatter)
    logger.addHandler(consoleHandler)
    return logger

class Threshold:
    def __init__(self):
        self.section = 'vertica_prod'
        self.json_file = 'validation_query.json'
        self.file_name=0
        self.logger= logger()
    
    def getconfig(self,section,key):
    
        parser = ConfigParser()
        parser.read(os.path.join(os.path.expanduser("~"),'.sharecare/credentials.cfg'))
        return parser.get(section,key)  
    
    def send_mail(self,receivers_email,mail_content,subject=None,data=None,html_template=None):
        mail = smtplib.SMTP('smtp.gmail.com', 587)
        mail.starttls()
        message = MIMEMultipart('mixed')
        message['From'] = self.getconfig("email","sender")
        message['To'] = ",".join([str(i) for i in receivers_email])
        message['Subject'] = subject
        message.attach(MIMEText(mail_content, 'plain'))
        
        if html_template is not None:
            enviornment_var = Environment(loader=FileSystemLoader('templates/'))
            content_data={}
            df=pd.DataFrame.from_dict(data)
            content_data["student_data"]=df.to_dict("records")
            content_data["columns"]=list(df.columns)
            mail_template = enviornment_var.get_template(f"{html_template}.html")
            html = mail_template.render(content_data=content_data)
            message.attach(MIMEText(html, 'html'))

        body = message.as_string()
        mail.login(self.getconfig("email","sender"),self.getconfig("email","password"))
        mail.sendmail(self.getconfig("email","sender"), receivers_email,body)
        mail.quit()


    def db_config(self,filename):
        if sys.platform=='win32':
            filename = os.getcwd()+''+'\\configs\\.sharecare\\credentials.cfg'  
        else: 
            filename = os.path.expanduser('~') + '' + '/.sharecare/credentials.cfg'
                    
        # create parser and read ini configuration file
        parser = ConfigParser(interpolation=None)
        parser.read(filename)
        # get section
        db = {}
        if parser.has_section(self.section):
            items = parser.items(self.section)
            for item in items:
                db[item[0]] = item[1]
        else:
            raise Exception(f'{self.section} not found in the {filename} file')
        return db
    
    def execute_query(self,query_list,connection):
        try:
            cursor =connection.cursor()
            for query in query_list:
                cursor.execute(query)     
        except Exception as error :
           self.logger.error(f'Exception  arise as : {error}')
    
    def detect_outliers(self,row):
        if (row['validation_value'] >= row['lower_range']) and (row['validation_value'] <= row['upper_range']) :
            return 'PASS'
        else:
            return 'DANGER'

    def get_metric_list(self,manual_run_specs):
        str_metric_list ="("
        for index,metric_id in enumerate(manual_run_specs["metric_id"]):
            if index <len(manual_run_specs["metric_id"])-1:
                str_metric_list = str_metric_list +f"{metric_id},"
            else :
                str_metric_list = str_metric_list +f"{metric_id})"
        
        return str_metric_list

    def get_entity_query(self,manual_run_specs):
        entity_query=""""""
        for index,entity in enumerate(manual_run_specs["entity"]):
            if index <len(manual_run_specs['entity'])-1:
                entity_query=entity_query +f"select {entity} as reportgroupid union "
            else:
                entity_query=entity_query +f"select {entity} as reportgroupid"
        return  entity_query

    
    def get_validation_range(self,tup,df):
        df_new=df[['metric_id','entity','dims']].head(1)
        
        data =list(df['validation_value'])
        Q2 = np.percentile(data, 50, interpolation = 'midpoint')


        q3_list = [a for a in data if a>Q2]
        q1_list = [a for a in data if a<Q2]
  
        if len(q3_list)>0:
            Q3 = np.percentile(q3_list, 50, interpolation = 'midpoint')
        else :
            Q3 = 0
  
        if len(q1_list)>0:
            Q1 = np.percentile(q1_list, 50, interpolation = 'midpoint')
        else :
            Q1=0
  
        IQR = Q3 - Q1
        upper = Q3 + 1.5*IQR
        lower = Q1 - 1.5*IQR
        df_new['upper_range'] = upper
        df_new['lower_range'] = lower

        return df_new
        

    def validate_missing_record(self,month_range,connection,dates,functional_area):
        df_missing_records =pd.DataFrame()

        self.logger.info('Executing the queries to get the percentage difference change between 2 consecutive months for last months ')
        for index,end_date in  enumerate(dates):
            self.logger.info(f'Executing for reporting_end_period : {end_date} and merged into the dataframe')
            query_list = []
            query_list.append("DROP TABLE IF EXISTS   metrics_metadata;")
            metrics_metadata = self.get_metrics_metadata(manual_run_specs,end_date,functional_area)
            query_list.append(metrics_metadata)

            self.execute_query(query_list,connection)

            query_diff ='''select entity,a.metric_id,to_char(a.reporting_end_period,'yyyy-mm') month_ending
            from sc_kpi.metrics_values a join metrics_metadata  m on a.metric_id =m.metric_id and 
            a.entity =m.reportgroupid  and to_char(a.reporting_end_period,'yyyy-mm')  =to_char(m.reporting_end_period,'yyyy-mm') 
            where a.entity::int in (select reportgroupid::int from elig) 
            group by 1,2,3 having max(metric_value) is null  and min(metric_value)  is null  '''

            df_null_values=pd.read_sql(query_diff,connection)
            df_missing_records=df_missing_records.append(df_null_values)
        
        # entity_df =pd.read_csv('elig_entity.csv',sep='|')
        # entity_df['entity']=  entity_df['entity'].astype(int)
        df_missing_records['entity']=  df_missing_records['entity'].astype(int)
        # df_missing_records = pd.merge(entity_df,df_missing_records,how='inner',on =['entity'])

        max_metric_value_query =f"""select entity ,metric_id ,max(metric_value) max_met,min(metric_value) as min_met from sc_kpi.metrics_values where functional_area ='{functional_area}' group by 1,2"""
        df_max_metric = pd.read_sql(max_metric_value_query,connection)
        

        df_missing_month = df_missing_records.groupby(['entity','metric_id'])['month_ending'].apply(','.join).reset_index()
        df_missing_month=df_missing_month.rename(columns={'month_ending':'Missing_month'})
        # print(df_missing_month)
        
        if not(df_missing_month.empty):
            df_mean =df_missing_records.groupby(['metric_id','entity'])
            df_missing_records =pd.DataFrame()
            for i in df_mean:
                df_1 = i[1][['entity','metric_id']].head(1)
                df_1['count'] = len(i[1])
                
                df_missing_records =df_missing_records.append(df_1)
            df_missing_records=df_missing_records[df_missing_records['count']!=month_range]
            df_missing_records.reset_index(inplace=True,drop=True)
            df_missing_records = pd.merge(df_missing_records,df_missing_month,how='left',on =['entity','metric_id'])
            df_missing_records.sort_values(by=['count'])
        df_max_metric['metric_id']=df_max_metric['metric_id'].astype(int)
        df_max_metric['entity']=df_max_metric['entity'].astype(int)
        df_missing_records =pd.merge(df_missing_records,df_max_metric,how='left',on =['entity','metric_id'])
        
        
        df_missing_records =df_missing_records.dropna(subset=['max_met'])
        df_missing_records = df_missing_records[df_missing_records['max_met']!=0]
        df_missing_records['consectutive_month'] =df_missing_records.apply(self.detect_consecutive_months,dates=dates, axis=1)
        df_missing_records=df_missing_records.sort_values(by=['max_met'])
        df_missing_records = df_missing_records[(df_missing_records['min_met']>=20) & (df_missing_records['max_met']>=50)]
        df_missing_records = df_missing_records[~(df_missing_records['consectutive_month'])]
        df_missing_records.to_csv('missing_records.csv',sep='|',index=False)

           
    def detect_consecutive_months(self,row,dates=[]):
        dates = list(map(lambda x:x[0:7],dates))
        dates = ','.join(dates)
        if row['Missing_month'] in dates and row['count']<=5:
            return False
        else:
            return True

    def get_date_list(self,end,month_range):
        list_date=[end.strftime("%Y-%m-%d")]
        first = end.replace(day=1)
        for i in range(month_range-1):
            last_month = first - timedelta(days=1)
            list_date.append(last_month.strftime("%Y-%m-%d"))
            first = last_month.replace(day=1)
        return list_date

    def elig_query(self,reporting_end_period):
        
        elig_1 = f"""CREATE LOCAL TEMP TABLE elig_1 ON COMMIT PRESERVE ROWS AS
                SELECT DISTINCT em.reportgroupid,egr.reportgroupname, em.guid,sem.secure_id
                FROM bi_reporting.eliggroupingmembers em
                JOIN sharecare.sc_employer_membership sem ON em.guid::varchar(100) = sem.guid::varchar(100) 
                join bi_reporting.eliggroupingrules egr on egr.reportgroupid = em.reportgroupid 
                where em.bienddate>'{reporting_end_period}'::date AND sem.deleted_flg IS NULL   and egr.isactive=1     
                ;"""
        elig = """CREATE LOCAL TEMP TABLE elig ON COMMIT PRESERVE ROWS AS
                select distinct el.reportgroupid,reportgroupname,count(distinct cc.secure_id) as tests
                from elig_1 el
                left join sharecare.sc_assessment_history_ratm cc
                        on (el.secure_id=cc.secure_id                      
                                and to_char(cc.creation_date,'yyyy-mm') >= to_char(add_months(sysdate,-18),'yyyy-mm')
                                and to_char(cc.creation_date,'yyyy-mm') <= to_char(add_months(sysdate,-1),'yyyy-mm'))
                group by 1,2;
                """
        
        return ["drop table if exists elig_1","drop table if exists elig_1",elig_1 ,elig]

    def validate_reportgroupid(self,reporting_end_period,connection):
        query= f""" select b.* from (select distinct reportgroupid from elig where  (tests >=50 or reportgroupid =9500035)) a left join ( select entity,count(*) as met_cnt,case when  count(*) =5 then 'PASS' else 'DANGER' end validation_result from 
           ( select entity,metric_id,metric_value from sc_kpi.metrics_values
             where metric_id in (100001,100002,100003,100007,1000020) and to_char(reporting_end_period,'yyyy-mm')=to_char('{reporting_end_period}'::date,'yyyy-mm')
             and entity::varchar(100) in (select distinct reportgroupid from elig where  (tests >=50 or reportgroupid =9500035))  and metric_value is not null) a
                    group by 1) b on a.reportgroupid=b.entity"""
        
      
        elig_member_query = self.elig_query(reporting_end_period)
        self.execute_query(elig_member_query ,connection)
        entity_df=pd.read_sql(query,connection)
        entity_df =entity_df[entity_df['entity']!=0]

        null_metric_id_query =f"""select entity,metric_id from sc_kpi.metrics_values
        where metric_id in (100001,100002,100003,100007,1000020) and to_char(reporting_end_period,'yyyy-mm')=to_char('{reporting_end_period}'::date,'yyyy-mm')
             and entity::varchar(100) in (select distinct reportgroupid from elig where  (tests >=50 or reportgroupid =9500035))  and metric_value is  null"""
        df_elig=pd.read_sql(null_metric_id_query,connection)
            
            
        df_elig['metric_id'] = df_elig['metric_id'].astype(str)
        df_elig = df_elig.groupby('entity')['metric_id'].apply(','.join).reset_index()
        df = pd.merge(entity_df,df_elig,how='left',on =['entity'])

        return df


    def get_metrics_metadata(self,manual_run_specs,reporting_end_period,functional_area) :
        if  manual_run_specs =={}:
            if functional_area == None:
                raise Exception('No functional area or metric_id is given')
            metrics_metadata =f"""CREATE LOCAL TEMP TABLE metrics_metadata ON COMMIT PRESERVE ROWS  As 
                select metric_id,reportgroupid,functional_area,'{reporting_end_period}'::date  as reporting_end_period,case when metric_id::int in (100001,100002,100003,1000049,10000101,100001803,100001804,100002033,100002038,100002069,100002073,100002100,100002114,100002115,100003003,100003006,100003044,100003045,100003062,100003063,100005006,100005007,100005017,100005018,100005021,100005022,100005037,100005040,100002024,100005153,100005063,100005028,100005065,100005044,1000017,100005086,100005023) then  'Monthly' else 'Lifetime' end metric_id_type  from sc_kpi.metrics_metadata a
                cross join (select distinct reportgroupid from bi_reporting.eliggroupingrules) b
                where functional_area = '{functional_area}';"""
            
        else :
            if manual_run_specs["metric_id"] and manual_run_specs["entity"]:
                str_metric_list =self.get_metric_list(manual_run_specs)
                metric_id_query =f"""select metric_id,reportgroupid,functional_area,'{reporting_end_period}'::date  as reporting_end_period,case when metric_id::int in (100001,100002,100003,1000049,10000101,100001803,100001804,100002033,100002038,100002069,100002073,100002100,100002114,100002115,100003003,100003006,100003044,100003045,100003062,100003063,100005006,100005007,100005017,100005018,100005021,100005022,100005037,100005040,100002024,100005153,100005063,100005028,100005065,100005044,1000017,100005086,100005023) then  'Monthly' else 'Lifetime' end metric_id_type   from  
                sc_kpi.metrics_metadata  """
                
                entity_query =self.get_entity_query(manual_run_specs)
                metrics_metadata=f"""
                CREATE LOCAL TEMP TABLE metrics_metadata ON COMMIT PRESERVE ROWS  As  {metric_id_query} a 
                cross join ({entity_query}) b where metric_id in 
                {str_metric_list}"""
                
            elif  manual_run_specs["metric_id"] != None  and manual_run_specs["entity"]==None:
                str_metric_list =self.get_metric_list(manual_run_specs)
                metric_id_query =f"""select  metric_id,reportgroupid,functional_area ,'{reporting_end_period}'::date
                     as reporting_end_period,case when metric_id::int in (100001,100002,100003,1000049,10000101,100001803,100001804,100002033,100002038,100002069,100002073,100002100,100002114,100002115,100003003,100003006,100003044,100003045,100003062,100003063,100005006,100005007,100005017,100005018,100005021,100005022,100005037,100005040,100002024,100005153,100005063,100005028,100005065,100005044,1000017,100005086,100005023) then  'Monthly' else 'Lifetime' end metric_id_type   from  sc_kpi.metrics_metadata"""
                metrics_metadata =f"""CREATE LOCAL TEMP TABLE metrics_metadata ON COMMIT PRESERVE ROWS  As 
                    {metric_id_query}  a cross join (select distinct reportgroupid from bi_reporting.eliggroupingrules where isactive = 1 ) b
                    where metric_id in  {str_metric_list}
                    """
            
            elif manual_run_specs["metric_id"] == None  and manual_run_specs["entity"]!=None:
                if functional_area == None:
                    raise Exception('No functional area or metric_id is given')
                entity_query =self.get_entity_query(manual_run_specs)
                metrics_metadata =f""" CREATE LOCAL TEMP TABLE metrics_metadata ON COMMIT PRESERVE ROWS  As 
                    select metric_id,reportgroupid,functional_area,'{reporting_end_period}'::date as reporting_end_period ,case when metric_id::int in (100001,100002,100003,1000049,10000101,100001803,100001804,100002033,100002038,100002069,100002073,100002100,100002114,100002115,100003003,100003006,100003044,100003045,100003062,100003063,100005006,100005007,100005017,100005018,100005021,100005022,100005037,100005040,100002024,100005153,100005063,100005028,100005065,100005044,1000017,100005086,100005023) then  'Monthly' else 'Lifetime' end metric_id_type  
                    from  sc_kpi.metrics_metadata a cross join ({entity_query}) b
                    where a.functional_area = '{functional_area}'"""
        return metrics_metadata


    def get_query(self):
        query =["DROP TABLE IF EXISTS   kpi_validation  ;"]

        
        query_lifetime_metric ="""create local temp table kpi_validation  on commit preserve rows as
            with run_params_cte as (select distinct reporting_end_period from  metrics_metadata)  
            select  distinct
                a.metric_id,
                a.dims,
                a.entity,
                a.functional_area,
                m.metric_id_type,
                to_char(a.reporting_end_period,'yyyy-mm') month_ending,
                a.metric_value,
                a.metric_value-b.metric_value as validation_value
                from  metrics_metadata  m
                full outer join sc_kpi.metrics_values a  on a.metric_id=m.metric_id and a.functional_area=m.functional_area  and a.entity=m.reportgroupid
                full outer join sc_kpi.metrics_values b  on a.entity=b.entity and a.metric_id=b.metric_id and nvl(a.dims,'aaa') = nvl(b.dims, 'aaa') and b.functional_area=m.functional_area
                join run_params_cte as r on to_char(b.reporting_end_period,'yyyy-mm') = to_char(add_months(r.reporting_end_period,-1),'yyyy-mm')
                and a.metric_value is not null and b.metric_value is not null
                where  metric_id_type = 'Lifetime' and  to_char(a.reporting_end_period,'yyyy-mm') =to_char(r.reporting_end_period,'yyyy-mm')  and b.metric_value<>0
                order by 1,2,4"""
        
        
        query_monthly_metric  ="""insert into  kpi_validation 
            with run_params_cte as (select distinct reporting_end_period from  metrics_metadata)  
            select  distinct
                a.metric_id,
                a.dims,
                a.entity,
                a.functional_area,
                m.metric_id_type,
                to_char(a.reporting_end_period,'yyyy-mm') month_ending,
                a.metric_value,
                a.metric_value   validation_value     
                from  metrics_metadata  m
                join sc_kpi.metrics_values a  on a.metric_id=m.metric_id and a.functional_area=m.functional_area  and a.entity=m.reportgroupid and m.metric_id_type='Monthly'
                join run_params_cte as r on  to_char(a.reporting_end_period,'yyyy-mm') =to_char(r.reporting_end_period,'yyyy-mm')  and a.metric_value<>0 and a.metric_value is not null
                order by 1,2,4"""

        query.append(query_lifetime_metric)
        query.append(query_monthly_metric)
        return query 
    
    def validate_records(self,dates,connection,functional_area,manual_run_specs):

        final_merged =pd.DataFrame()

        self.logger.info('Executing the queries to get the percentage difference change between 2 consecutive months for last months ')
        for index,end_date in  enumerate(dates):
            self.logger.info(f'Executing for reporting_end_period : {end_date} and merged into the dataframe')
            query_list = []
            query_list.append("DROP TABLE IF EXISTS   metrics_metadata;")
            metrics_metadata = self.get_metrics_metadata(manual_run_specs,end_date,functional_area)
            query_list.append(metrics_metadata)
                
            query = self.get_query()
            query_list=query_list+query
            self.execute_query(query_list,connection)

            query_diff ='''select metric_id,dims,entity,functional_area,metric_id_type,month_ending,metric_value, validation_value from kpi_validation '''
                
            df=pd.read_sql(query_diff,connection)
            final_merged=final_merged.append(df)

            # print(final_merged)
            #  To replace null in dims with

        final_merged['dims'] = final_merged['dims'].fillna(value=np.nan)
        final_merged['dims'] = final_merged['dims'].replace(np.nan, 'abc', regex=True)
        final_merged['dims'] =final_merged['dims'].replace('','abc',)
            
        self.logger.info("calculating  upper_range and lower range for record group by metric_id,dims and entity")
        groups_list =final_merged.groupby(['metric_id','dims','entity'])
            
            
        df_validaion_range=pd.DataFrame()
        for groups in groups_list:
            group = groups[0]
            df_group = groups[1]
            if len(df_group)>=6:
                df_group=df_group.sort_values(by=['validation_value'], ascending=True)
                df_group_range= self.get_validation_range(group,df_group)
            else:
                continue
            df_validaion_range=df_validaion_range.append(df_group_range)
            

        validation_result = pd.merge(final_merged, df_validaion_range , on=['metric_id', 'entity','dims'])
            
        validation_result['validation_result'] = validation_result.apply(self.detect_outliers, axis=1)
        return validation_result

    def main(self,reporting_end_period,month_range,manual_run_specs,functional_area=None):
        try: 
            self.logger.info('Get vertica database credential')
            db=self.db_config('credentials.cfg')
            self.logger.info('Get vertica database connection')
            connection = vertica_python.connect(**db)
            
            self.logger.info(f'Get the reporting end period for last {month_range} months ')
            format='%Y-%m-%d'
            end = datetime.strptime(reporting_end_period,format)
            dates =self.get_date_list(end,month_range)
            # print(dates)

            # df_entity = self.validate_reportgroupid(reporting_end_period,connection)
           
            self.validate_missing_record(month_range,connection,dates,functional_area)

            # validation_result =self.validate_records(dates,connection,functional_area,manual_run_specs)
            # validation_result =validation_result[['metric_id','dims','entity','functional_area','metric_id_type','month_ending','metric_value','validation_result']]
            
            # validation_result.to_csv("result.csv",sep="|" ,index =False)
            # month_list =['2022-11']
            # validation_result =validation_result[validation_result['month_ending_m2'].isin(month_list)]
            # validation_result.to_csv(f"{functional_area}_result.csv",sep="|" ,index =False)
            # outliers =validation_result[validation_result['validation_result']=='DANGER']
            # print(validation_result)
            # data =outliers.to_dict('records')
            # mail_content='''Hello, This a sample email contain outlier   in QBR'''
            # subject='outliers'
            # receivers_email=["abhinavkumar1243@gmail.com"]
            
            # self.send_mail(receivers_email,mail_content,subject=subject,html_template='mail',data=data)
                        
        except Exception as  exception:
           self.logger.error(f'Exception  arise as : {exception}')
           raise exception
        
if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-func','--functional_area',help='Functional area to execute.',required=False)
    parser.add_argument('-range','--months',help='number of months ',type =int,required=True)
    parser.add_argument('-end','--reporting_end_period',help='End of reporting period for  run.',required=True)
    parser.add_argument('-ent','--entity' ,type=int,nargs='+',help='Functional area to execute.',required=False)
    parser.add_argument('-met','--metric_id',nargs='+',help='Functional area to execute.',required=False)
   
    args, unknown = parser.parse_known_args()
    args = vars(args)

    if args['functional_area']:
        functional_area=args['functional_area']
    else:
        functional_area=None

    reporting_end_period=args['reporting_end_period']
    no_of_months=args['months']
    manual_run_specs = {}
    optional_args = ['entity','metric_id']

    manual_options = 0
    for optional in optional_args:
        if args[optional]:
            manual_options+=1

    if manual_options > 0:
        manual_run_specs = {'entity':None,'metric_id':None}
        for optional in optional_args:
            if optional == 'metrics':
                if args[optional]:
                    if type(args[optional]) == tuple:
                        args[optional] = list(args[optional])
                    elif type(args[optional]) != list:
                        args[optional] = [args[optional]]
            manual_run_specs[optional] = args[optional]

        if manual_run_specs['metric_id'] is not None:
            for i in range(0, len(manual_run_specs['metric_id'])):
                manual_run_specs['metric_id'][i] = int(manual_run_specs['metric_id'][i])
            
        if manual_run_specs['entity'] is not None:
            for i in range(0, len(manual_run_specs['entity'])):
                manual_run_specs['entity'][i] = int(manual_run_specs['entity'][i])
            
    try:
        validation=Threshold()
        validation.main(reporting_end_period,no_of_months,manual_run_specs,functional_area=functional_area)

        validation.logger.info('successfully executed......')
    except Exception as exception:
        validation.logger.error(f'Exception arise as {exception}')




    