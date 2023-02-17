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

class Kpi_qbr_validation:
    def __init__(self):
        self.section = 'vertica_prod'
        self.json_file = 'validation_query.json'
        self.file_name=0
        self.logger= logger()
        self.df_elig_ent =pd.DataFrame()
        self.dates=[]
    
    def getconfig(self,section,key):
    
        parser = ConfigParser()
        parser.read(os.path.join(os.path.expanduser("~"),'.sharecare/credentials.cfg'))
        return parser.get(section,key)  
    
    def send_mail(self,receivers_email,mail_content,subject=None,df_list=[],functional_area='Manual',files_name=[],html_template=None,description=''):
        mail = smtplib.SMTP('smtp.gmail.com', 587)
        mail.starttls()
        message = MIMEMultipart('mixed')
        message['From'] = self.getconfig("email","sender")
        message['To'] = ",".join([str(i) for i in receivers_email])
        message['Subject'] = subject
        message.attach(MIMEText(description, 'plain'))

        if html_template is not None:
            enviornment_var = Environment(loader=FileSystemLoader('templates/'))
            outliers={}
            missing_month={}
            # df=pd.DataFrame.from_dict(data)
            outliers["data"]=df_list[0].to_dict("records")
            outliers["columns"]=list(df_list[0].columns)

            missing_month["data"]=df_list[1].to_dict("records")
            missing_month["columns"]=list(df_list[1].columns)

            mail_template = enviornment_var.get_template(f"{html_template}.html")
            # var= {'content_data':content_data}
            html = mail_template.render(outliers=outliers,missing_month=missing_month,functional_area=functional_area,description=description)
            message.attach(MIMEText(html, 'html'))
        
        for files in files_name:
            attach_file_name = f"{files}"
            attach_file = open(attach_file_name, 'rb')
            payload = MIMEBase('application', "octet-stream")
            payload.set_payload((attach_file).read())
            encoders.encode_base64(payload) 

            payload.add_header(
                "Content-Disposition",
                f"attachment; filename= {files}",
            )
            message.attach(payload)

        
        
        body = message.as_string()
        h1='h12332'
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
        
    def get_lifetime_dates(self,dates):
        dates = list(map(lambda x:x[0:7],dates))
        # dates = ','.join(dates)
        rep=reporting_end_period[:7]
        year=rep[0:4]
        month=rep[5:]
        list_q=[]
        dates =dates[0:4]
        for i in dates:
            if i[5:] in ['12','09','06','03'] :
                list_q.append(i)

        date=[]
        for i in dates:
            if i in  list_q:
                date.append(i)
        
        list_dates =dates.copy()
        dates=[]
        for  i in  list_dates:
            if i >=date[-1]:
                dates.append(i)
        return dates

    def validate_missing_record(self,month_range,connection,functional_area,elig_entity):
        df_missing_records =pd.DataFrame()
        format='%Y-%m-%d'
        end = datetime.strptime(reporting_end_period,format)
        dates =self.get_date_list(end,15)

        self.logger.info('Executing the queries to get the percentage difference change between 2 consecutive months for last months ')
        for index,end_date in  enumerate(dates):
            self.logger.info(f'Executing for reporting_end_period : {end_date} and merged into the dataframe')
            query_list = []
            query_list.append("DROP TABLE IF EXISTS   metrics_metadata;")
            metrics_metadata = self.get_metrics_metadata(manual_run_specs,end_date,functional_area)
            query_list.append(metrics_metadata)
            

            self.execute_query(query_list,connection)
           

            query_diff ='''select a.functional_area,m.metric_id_type,entity,a.metric_id,nvl(a.dims,'abc') dims,to_char(a.reporting_end_period,'yyyy-mm') month_ending
            from sc_kpi.metrics_values a join metrics_metadata  m on a.metric_id =m.metric_id and  m.metric_id_type='Monthly' and  nullif(m.dims,'') is null 
            and a.entity =m.reportgroupid  and to_char(a.reporting_end_period,'yyyy-mm')  =to_char(m.reporting_end_period,'yyyy-mm') 
            where a.entity::int in (select reportgroupid::int from elig) 
            group by 1,2,3,4,5,6 having max(metric_value) is null  and min(metric_value)  is null  '''

            # query_diff ='''select a.functional_area,m.metric_id_type,entity,a.metric_id,nvl(a.dims,'abc') dims,to_char(a.reporting_end_period,'yyyy-mm') month_ending
            # from sc_kpi.metrics_values a join metrics_metadata  m on a.metric_id =m.metric_id and m.metric_id_type='Monthly' and  nullif(m.dims,'') is   null 
            # and a.entity =m.reportgroupid  and to_char(a.reporting_end_period,'yyyy-mm')  =to_char(m.reporting_end_period,'yyyy-mm') 
           
            # group by 1,2,3,4,5,6 having max(metric_value) is null  and min(metric_value)  is null  '''

            query_diff ='''select a.functional_area,m.metric_id_type,entity,a.metric_id,nvl(a.dims,'abc') dims,to_char(a.reporting_end_period,'yyyy-mm') month_ending
            from sc_kpi.metrics_values a join metrics_metadata  m on a.metric_id =m.metric_id  and  nullif(m.dims,'') is   null 
            and a.entity =m.reportgroupid  and to_char(a.reporting_end_period,'yyyy-mm')  =to_char(m.reporting_end_period,'yyyy-mm') 
           
            group by 1,2,3,4,5,6 having max(metric_value) is null  and min(metric_value)  is null  '''

            df_null_values=pd.read_sql(query_diff,connection)
            # print(df_null_values)
            df_missing_records=df_missing_records.append(df_null_values)
        
        if not(df_missing_records.empty):
            # entity_df =pd.read_csv('elig_entity.csv',sep='|')
            # entity_df['entity']=  entity_df['entity'].astype(int)
            # df_missing_records['entity']=  df_missing_records['entity'].astype(int)
            # df_missing_records = pd.merge(entity_df,df_missing_records,how='inner',on =['entity'])

            elig_entity['entity']=  elig_entity['entity'].astype(int)
            df_missing_records['entity']=  df_missing_records['entity'].astype(int)
            df_missing_records = pd.merge(elig_entity,df_missing_records,how='inner',on =['entity'])

            max_metric_value_query =f"""select entity ,nvl(dims,'abc') dims,metric_id ,max(metric_value) max_met,min(metric_value) as min_met from sc_kpi.metrics_values where functional_area in (select distinct functional_area from metrics_metadata) group by 1,2,3"""
            df_max_metric = pd.read_sql(max_metric_value_query,connection)
             
            

            df_missing_month = df_missing_records.groupby(['entity','metric_id','dims'])['month_ending'].apply(','.join).reset_index()
            df_missing_month=df_missing_month.rename(columns={'month_ending':'Missing_month'})
            
        else :
            df_missing_month= pd.DataFrame()

     
        
        if not(df_missing_month.empty):
            df_mean =df_missing_records.groupby(['entity','metric_id','dims'])
            df_missing_records =pd.DataFrame()
            for i in df_mean:
                df_1 = i[1][['functional_area','metric_id_type','entity','metric_id','dims']].head(1)
                df_1['count'] = len(i[1])
                
                df_missing_records =df_missing_records.append(df_1)
            df_missing_records=df_missing_records[df_missing_records['count']!=month_range]
            df_missing_records.reset_index(inplace=True,drop=True)
            df_missing_records = pd.merge(df_missing_records,df_missing_month,how='left',on =['entity','metric_id','dims'])
            df_missing_records.sort_values(by=['count'])
            
            df_max_metric['metric_id']=df_max_metric['metric_id'].astype(int)
            df_max_metric['entity']=df_max_metric['entity'].astype(int)
            df_missing_records = pd.merge(df_missing_records,df_max_metric,how='left',on =['entity','metric_id','dims'])
            # 
            df_missing_records = df_missing_records.dropna(subset=['max_met'])
            

        # print(df_missing_records) 
        if not(df_missing_records.empty):
            df_missing_records = df_missing_records[df_missing_records['max_met']!=0]
            
            dates = list(map(lambda x:x[0:7],dates))
            dates = ','.join(dates)
            
            df_missing_records['consectutive_month'] =df_missing_records.apply(self.detect_consecutive_months,dates=dates, axis=1)
    

            df_missing_records = df_missing_records[~(df_missing_records['consectutive_month'])]
            elig_entity['entity'] = elig_entity['entity'].astype(int)
            df_missing_records = pd.merge(df_missing_records,elig_entity,how='inner',on =['entity'])
            df_missing_records =df_missing_records.drop(columns='consectutive_month')
            
        
        return df_missing_records

    def validate_missing_dims(self,month_range,connection,functional_area,elig_entity):
        df_missing_records =pd.DataFrame()
        format='%Y-%m-%d'
        end = datetime.strptime(reporting_end_period,format)
        dates =self.get_date_list(end,15)
        query_list = []
        query_list.append("DROP TABLE IF EXISTS   metrics_metadata;")
        metrics_metadata = self.get_metrics_metadata(manual_run_specs,dates[0],functional_area)
        query_list.append(metrics_metadata)
        # print(query_list[1])
        self.execute_query(query_list,connection)
        query= """select distinct m.metric_id_type,a.functional_area,a.metric_id,a.entity, a.dims from sc_kpi.metrics_values  a join 
        (select metric_id_type,functional_area,reportgroupid,metric_id from metrics_metadata m 
        where nullif(m.dims,'') is not  null  and metric_id_type ='Monthly') m on a.entity =m.reportgroupid and a.metric_id =m.metric_id
        and dims is not null"""
        
        query= """select distinct m.metric_id_type,a.functional_area,a.metric_id,a.entity, a.dims from sc_kpi.metrics_values  a join 
        (select metric_id_type,functional_area,reportgroupid,metric_id from metrics_metadata m 
        where nullif(m.dims,'') is not  null  ) m on a.entity =m.reportgroupid and a.metric_id =m.metric_id
        and dims is not null"""
        df= pd.read_sql(query,connection)
        # entity_df =pd.read_csv('elig_entity.csv',sep='|')
       
        df['entity']=  df['entity'].astype(int)
        df = pd.merge(elig_entity,df,how='inner',on =['entity'])
        # print(df)
        df_grp=df.groupby(['metric_id_type','functional_area','entity','metric_id'])
        

        for row in df_grp:
            functional_area=row[0][1]
            metric_id_type=row[0][0]
            entity =row[0][2]
            metric_id= row[0][3]

            dims_list = list(row[1]['dims'].dropna())
            
            dims_val="','".join([str(i).replace("'","''") for i in dims_list])
            dims_val =f"('{dims_val}')"
            if metric_id_type=='Montly':
                for index,end_date in  enumerate(dates):
                    
                    query = f"""select distinct dims from sc_kpi.metrics_values where entity = {entity} and 
                    to_char(reporting_end_period,'yyyy-mm')=to_char('{end_date}'::date,'yyyy-mm') and metric_id ={metric_id} 
                    and dims IN {dims_val}
                    and metric_Value is not null"""
                    
                    dims_df =pd.read_sql(query,connection)
                    dims=list(dims_df['dims'])
                    
                    dims_null=[]
                    for i in dims_list:
                        # print(i)
                        if i not in dims:
                            dims_null.append(i)
                    # print(dims_null)
                    df_missing_dims =pd.DataFrame({'functional_area':[functional_area],'metric_id_type':[metric_id_type],'metric_id':[metric_id],'entity':[entity],'dims':[dims_null],'Missing_month':[end_date[0:7]]})
                    df_missing_records =df_missing_records.append(df_missing_dims)
            else:
                dates=self.get_lifetime_dates(dates)
                
                for index,end_date in  enumerate(dates[0:4]):
                
                    query = f"""select distinct dims from sc_kpi.metrics_values where entity = {entity} and 
                    to_char(reporting_end_period,'yyyy-mm')='{end_date}'
                    and metric_id ={metric_id} 
                    and dims IN {dims_val}
                    and metric_Value is not null"""
                    
                    dims_df =pd.read_sql(query,connection)
                    dims=list(dims_df['dims'])
                    
                    dims_null=[]
                    for i in dims_list:
                        # print(i)
                        if i not in dims:
                            dims_null.append(i)
                    # print(dims_null)
                    df_missing_dims =pd.DataFrame({'functional_area':[functional_area],'metric_id_type':[metric_id_type],'metric_id':[metric_id],'entity':[entity],'dims':[dims_null],'Missing_month':[end_date[0:7]]})
                    df_missing_records =df_missing_records.append(df_missing_dims)
                

      
            
        if not(df_missing_records.empty):
            
            
            elig_entity['entity']=  elig_entity['entity'].astype(int)
            df_missing_records['entity']=  df_missing_records['entity'].astype(int)
            df_missing_records = pd.merge(elig_entity,df_missing_records,how='inner',on =['entity'])

            

            max_metric_value_query =f"""select entity ,nvl(dims,'abc') dims,metric_id ,max(metric_value) max_met,min(metric_value) as min_met from sc_kpi.metrics_values where functional_area in (select distinct functional_area from metrics_metadata) group by 1,2,3"""
            df_max_metric = pd.read_sql(max_metric_value_query,connection)
            df_missing_records=df_missing_records.explode('dims')
            
            
            df_missing_month= df_missing_records.groupby(['entity','metric_id','dims'])['Missing_month'].apply(','.join).reset_index()
            
            
        else :
            df_missing_month= pd.DataFrame()
        if not(df_missing_month.empty):
            df_mean =df_missing_records.groupby(['entity','metric_id','dims'])
            df_missing_records =pd.DataFrame()
            for i in df_mean:
                df_1 = i[1][['functional_area','metric_id_type','entity','metric_id','dims']].head(1)
                df_1['count'] = len(i[1])
                
                df_missing_records =df_missing_records.append(df_1)
            df_missing_records=df_missing_records[df_missing_records['count']!=month_range]
            df_missing_records.reset_index(inplace=True,drop=True)
            df_missing_records = pd.merge(df_missing_records,df_missing_month,how='left',on =['entity','metric_id','dims'])
            df_missing_records.sort_values(by=['count'])
            
            df_max_metric['metric_id']=df_max_metric['metric_id'].astype(int)
            df_max_metric['entity']=df_max_metric['entity'].astype(int)
            df_missing_records = pd.merge(df_missing_records,df_max_metric,how='left',on =['entity','metric_id','dims'])
            df_missing_records = df_missing_records.dropna(subset=['max_met'])
            

        # print(df_missing_records) 
        if not(df_missing_records.empty):
            df_missing_records = df_missing_records[df_missing_records['max_met']!=0]
            
            dates = list(map(lambda x:x[0:7],dates))
            dates = ','.join(dates)
            
            df_missing_records['consectutive_month'] =df_missing_records.apply(self.detect_consecutive_months,dates=dates, axis=1)
            
            df_missing_records = df_missing_records[~(df_missing_records['consectutive_month'])]
            elig_entity['entity'] = elig_entity['entity'].astype(int)
            df_missing_records = pd.merge(df_missing_records,elig_entity,how='inner',on =['entity'])
            df_missing_records =df_missing_records.drop(columns='consectutive_month')
        
        
        df_missing_records.to_csv('dims.csv',sep='|',index =False)
        return df_missing_records
    

    def detect_consecutive_months(self,row,dates=''):
        
        # print(dates[-1])
        
        if row['Missing_month'] in dates and row['count']<=8 and dates[-7:]  not in row['Missing_month'] :
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
        
        query =f"""
        select a.entity,b.met_cnt,b.validation_result from (select distinct reportgroupid as entity from elig where  (tests >=50 or reportgroupid =9500035)) a left join ( select entity,count(*) as met_cnt,case when  count(*) =5 then 'PASS' else 'DANGER' end validation_result from 
           ( select entity,metric_id,metric_value from sc_kpi.metrics_values
             where metric_id in (100001,100002,100003,100007,1000020) and to_char(reporting_end_period,'yyyy-mm')=to_char('{reporting_end_period}'::date,'yyyy-mm')
             and entity::varchar(100) in (select distinct reportgroupid from elig where  (tests >=50 or reportgroupid =9500035))  and metric_value is not null) a
                    group by 1) b on a.entity=b.entity"""
        
      
        elig_member_query = self.elig_query(reporting_end_period)
        self.logger.info('Get query for eligible reortgroups')
        self.execute_query(elig_member_query ,connection)
        entity_df=pd.read_sql(query,connection)
        entity_df =entity_df[entity_df['entity']!=0]

        elig_1 = pd.read_sql('select distinct reportgroupid as entity from elig where  (tests >=50 or reportgroupid =9500035)',connection)
        elig_1.to_csv('dims.csv',sep='|',index=False)


        null_metric_id_query =f"""select entity,metric_id from sc_kpi.metrics_values
        where metric_id in (100001,100002,100003,100007,1000020) and to_char(reporting_end_period,'yyyy-mm')=to_char('{reporting_end_period}'::date,'yyyy-mm')
             and entity::varchar(100) in (select distinct reportgroupid from elig where  (tests >=50 or reportgroupid =9500035))  and metric_value is  null"""
        self.logger.info('execute the query to get the reportgroupid with key metric is null')
        df_elig=pd.read_sql(null_metric_id_query,connection)
            
            
        df_elig['metric_id'] = df_elig['metric_id'].astype(str)
        df_elig = df_elig.groupby('entity')['metric_id'].apply(','.join).reset_index()
        df_elig['entity'] = df_elig['entity'].astype(str)
        entity_df['entity'] = entity_df['entity'].astype(str)
        df = pd.merge(entity_df,df_elig,how='left',on =['entity'])
        # elig_1['entity'] = elig_1['entity'].astype(str)
        # df['entity'] = df['entity'].astype(str)
        # df = pd.merge(elig_1,df,how='left',on =['entity'])
        df_missing_entity=df.copy()

        df_missing_entity= df_missing_entity[(pd.isnull(df['met_cnt'])) & (pd.isnull(df['validation_result']))]
        df=df[~((pd.isnull(df['met_cnt'])) & (pd.isnull(df['validation_result'])))]
        df_missing_entity['met_cnt']=0
        df_missing_entity['metric_id']='100001,100002,100003,100007,1000020'
        df_missing_entity['validation_result']='DANGER'
        df=df.append(df_missing_entity)

        return df


    def get_metrics_metadata(self,manual_run_specs,reporting_end_period,functional_area) :
        ent_list= list(self.df_elig_ent['entity'].astype(int))
        ent_list=",".join([str(i) for i in ent_list])
        ent_list=f"({ent_list})"
        # print(ent_list)
        if  manual_run_specs =={}:
            if functional_area == None:
                raise Exception('No functional area or metric_id is given')
            metrics_metadata =f"""CREATE LOCAL TEMP TABLE metrics_metadata ON COMMIT PRESERVE ROWS  As 
                select metric_id,reportgroupid,functional_area,dims,'{reporting_end_period}'::date  as reporting_end_period,case when metric_id::int in (100001,100002,100003,1000049,10000101,100001803,100001804,100002033,100002038,100002069,100002073,100002100,100002114,100002115,100003003,100003006,100003044,100003045,100003062,100003063,100005006,100005007,100005017,100005018,100005021,100005022,100005037,100005040,100005153,100005063,100005028,100005065,100005044,1000017,100005086,100005023) then  'Monthly' else 'Lifetime' end metric_id_type  from sc_kpi.metrics_metadata a
                cross join (select distinct reportgroupid from bi_reporting.eliggroupingrules where reportgroupid::int in {ent_list}) b
                where functional_area = '{functional_area}';"""
            
        else :
            if manual_run_specs["metric_id"] and manual_run_specs["entity"]:
                str_metric_list =self.get_metric_list(manual_run_specs)
                metric_id_query =f"""select metric_id,reportgroupid,dims,functional_area,'{reporting_end_period}'::date  as reporting_end_period,case when metric_id::int in (100001,100002,100003,1000049,10000101,100001803,100001804,100002033,100002038,100002069,100002073,100002100,100002114,100002115,100003003,100003006,100003044,100003045,100003062,100003063,100005006,100005007,100005017,100005018,100005021,100005022,100005037,100005040,100005153,100005063,100005028,100005065,100005044,1000017,100005086,100005023) then  'Monthly' else 'Lifetime' end metric_id_type   from  
                sc_kpi.metrics_metadata  """
                
                entity_query =self.get_entity_query(manual_run_specs)
                metrics_metadata=f"""
                CREATE LOCAL TEMP TABLE metrics_metadata ON COMMIT PRESERVE ROWS  As  {metric_id_query} a 
                cross join ({entity_query}) b where metric_id in 
                {str_metric_list}"""
                
            elif  manual_run_specs["metric_id"] != None  and manual_run_specs["entity"]==None:
                str_metric_list =self.get_metric_list(manual_run_specs)
                metric_id_query =f"""select  metric_id,reportgroupid,dims,functional_area ,'{reporting_end_period}'::date
                     as reporting_end_period,case when metric_id::int in (100001,100002,100003,1000049,10000101,100001803,100001804,100002033,100002038,100002069,100002073,100002100,100002114,100002115,100003003,100003006,100003044,100003045,100003062,100003063,100005006,100005007,100005017,100005018,100005021,100005022,100005037,100005040,100005153,100005063,100005028,100005065,100005044,1000017,100005086,100005023) then  'Monthly' else 'Lifetime' end metric_id_type   from  sc_kpi.metrics_metadata"""
                metrics_metadata =f"""CREATE LOCAL TEMP TABLE metrics_metadata ON COMMIT PRESERVE ROWS  As 
                    {metric_id_query}  a cross join (select distinct reportgroupid from bi_reporting.eliggroupingrules where   reportgroupid::int in {ent_list} and isactive = 1 ) b
                    where metric_id in  {str_metric_list}
                    """
            
            elif manual_run_specs["metric_id"] == None  and manual_run_specs["entity"]!=None:
                if functional_area == None:
                    raise Exception('No functional area or metric_id is given')
                entity_query =self.get_entity_query(manual_run_specs)
                metrics_metadata =f""" CREATE LOCAL TEMP TABLE metrics_metadata ON COMMIT PRESERVE ROWS  As 
                    select metric_id,reportgroupid,functional_area,dims,'{reporting_end_period}'::date as reporting_end_period ,case when metric_id::int in (100001,100002,100003,1000049,10000101,100001803,100001804,100002033,100002038,100002069,100002073,100002100,100002114,100002115,100003003,100003006,100003044,100003045,100003062,100003063,100005006,100005007,100005017,100005018,100005021,100005022,100005037,100005040,100005153,100005063,100005028,100005065,100005044,1000017,100005086,100005023) then  'Monthly' else 'Lifetime' end metric_id_type  
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

    def css_to_rows(self,row,columns=''):
        list_month=row[columns].split(',')
        return list_month

    def remove_validated_records(self,df_missing_records,validation_result):
        if not(validation_result.empty):
            df_val_outliers= pd.read_csv('csv_files/outlier_validated_result.csv',sep='|')
            df_val_outliers_passed=df_val_outliers.copy()
            df_val_outliers_passed=df_val_outliers_passed[df_val_outliers_passed['validation_result']=='PASSED']
           
            df_val_outliers_passed['entity']=df_val_outliers_passed['entity'].astype('str')
            df_val_outliers['entity']=df_val_outliers['entity'].astype('str')
           
            validation_result=pd.merge(validation_result,df_val_outliers_passed, indicator=True, how='outer').query('_merge=="left_only"').drop('_merge', axis=1)
            
            df_val_outliers =df_val_outliers.append(validation_result)
            
            df_val_outliers=df_val_outliers[['metric_id','dims','entity','functional_area','metric_id_type','month_ending','metric_value','validation_result']]
            df_val_outliers.drop_duplicates(subset=['metric_id','dims','entity','functional_area','metric_id_type','month_ending','metric_value'],
                     keep='first', inplace=True)
            # print(df_val_outliers)
            df_val_outliers.to_csv('csv_files/outlier_validated_result.csv',sep='|',index=False)
        
        else:
            validation_result=pd.DataFrame()

        if not(df_missing_records.empty):
            df_val= pd.read_csv('csv_files/validated_result.csv',sep='|')
        
            df_missing =df_missing_records.copy()
            df_missing['month'] =df_missing.apply(self.css_to_rows,columns='Missing_month',axis=1)
            df_missing =df_missing[['metric_id_type','functional_area','entity','dims','metric_id','month']]
            df_missing=df_missing.explode(column='month')
            df_pass= df_val[df_val['validated']=='PASSED']

            df1=pd.merge(df_missing,df_pass, indicator=True, how='outer').query('_merge=="left_only"').drop('_merge', axis=1)
            df_val = df_val.append(df1)
            df_val= df_val[['functional_area','entity','metric_id','dims','metric_id_type','month','validated']]
            df_val.drop_duplicates(subset=['functional_area','entity','metric_id','dims','metric_id_type','month'],
                        keep='first', inplace=True)
            df_val.to_csv('csv_files/validated_result.csv',sep='|',index=False)

            df1 = df1.groupby(['functional_area','metric_id_type','entity','metric_id','dims'])['month'].apply(','.join).reset_index()
        else:
            df_1=pd.DataFrame()
        return df1,validation_result
    
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
        # print(validation_result)
        return validation_result

    def consecutive_quarter_lifetime(self,row):
        dates=self.get_lifetime_dates(self.dates)
        
        if dates[0] in row['Missing_month'] and dates[-1] in row['Missing_month']:
            return False
        else:
            return True

    def remove_threshold(self,row):
        if row['metric_value']>row['threshold']:
            return True
        else:
            return False

    def remove_previous_qaurt_null(self,df,connection,dates):
        dates=self.get_lifetime_dates(dates)
        df=df.reset_index(drop=True)
        
        # df=df_final_liftime.copy()
        df=df[['functional_area','metric_id_type','entity','metric_id','dims','Missing_month']]
       
        mask = df['Missing_month'].str.contains(dates[-1], na=True)
        
        
        df.loc[df.index, 'prevquarter'] = mask
        # df[ 'prevquarter']=mask
        df=df[df['prevquarter']==False]
        
     
        df=df[['functional_area','metric_id_type','entity','metric_id','dims','Missing_month']]
        mask = df['Missing_month'].str.contains(dates[0], na=True)
        # df=df.reset_index(drop=True)
        df.loc[df.index, 'prevquarter'] = mask
        # print(list(df.index))
        df=df[df['prevquarter']==True] 
        df=df.reset_index(drop=True)
        

        df_threshold=pd.read_csv('csv_files/threshold.csv',sep='|')

        # df_grp=df.groupby(['entity','metric_id','dims'])


        df_final_liftime = pd.DataFrame()

        for i,row in df.iterrows():
            
            functional_area=row['functional_area']
            missing_month=row['Missing_month']
            metric_id=row['metric_id']
            dims=row['dims']
            entity=row['entity']
            # print(metric_id)
            if dims=='abc':
                query =f'''select functional_area,'{row["metric_id_type"]}' as metric_id_type,entity,metric_id
                ,'abc' dims,'{missing_month}' as Missing_month ,metric_value from sc_kpi.metrics_values where metric_id ={metric_id}
                and entity={entity}  and to_char(reporting_end_period,'yyyy-mm')='{dates[-1]}' '''
                # print(query)
            else:
                query =f'''select functional_area,'{row["metric_id_type"]}' as metric_id_type,entity,metric_id
                ,dims,'{missing_month}' as Missing_month ,metric_value from sc_kpi.metrics_values where metric_id ={metric_id}
                and entity={entity} and dims='{dims}' and to_char(reporting_end_period,'yyyy-mm')='{dates[-1]}' '''
                # print(query)
            
            df_final_liftime = df_final_liftime.append(pd.read_sql(query,connection))



        df_final_liftime=pd.merge(df_final_liftime,df_threshold,how='left',on=['metric_id'])

        df_final_liftime['threshold'] = df_final_liftime['threshold'].fillna(value=np.nan)
        df_final_liftime['threshold'] = df_final_liftime['threshold'].replace(np.nan, 0, regex=True)
        df_final_liftime['above_thres'] =df_final_liftime.apply(self.remove_threshold,axis=1)
        df_final_liftime= df_final_liftime[df_final_liftime['above_thres']]
        # df_final_liftime.to_csv('lifetime_missing_record_test.csv',sep='|',index=False)
        return df_final_liftime


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
            self.dates=dates
            
            df_entity = self.validate_reportgroupid(reporting_end_period,connection)
            df_entity.to_csv('lvl1_val.csv',sep='|',index=False)

            # dates=self.get_lifetime_dates(dates)
            # print(dates)
            # df_entity = pd.read_csv('csv_files/lvl1_val.csv',sep='|')
            # df_lvl_1 =df_entity[df_entity['validation_result']=='DANGER']

            # elig_entity =df_entity[df_entity['validation_result']=='PASS']
            # elig_entity = elig_entity.dropna(subset=['entity'])
            # elig_entity =elig_entity['entity']
            # elig_entity= pd.DataFrame({'entity':elig_entity.values})
            # self.df_elig_ent=elig_entity

          
            """
            df_missing_records_1 = self.validate_missing_record(month_range,connection,functional_area,elig_entity)
            # print(df_missing_records_1)
            df_missing_records_2 = self.validate_missing_dims(month_range,connection,functional_area,elig_entity)
            
            df_missing_records =df_missing_records_1.append(df_missing_records_2)

            df_lifetime =df_missing_records[df_missing_records['metric_id_type']=='Lifetime']
            df_monthly =df_missing_records[df_missing_records['metric_id_type']=='Monthly']
            df_lifetime=df_lifetime.reset_index(drop=True)
            
            
            if not(df_lifetime.empty):
                df_lifetime.loc[df_lifetime.index,'consectutive_month'] =df_lifetime.apply(self.consecutive_quarter_lifetime, axis=1)
    
                df_lifetime=df_lifetime[df_lifetime['consectutive_month']==True]
                df_lifetime=self.remove_previous_qaurt_null(df_lifetime,connection,dates)
                
            
            
            df_lifetime =df_lifetime[['functional_area','metric_id_type','entity','metric_id','dims','Missing_month']]
            df_monthly=df_monthly[['functional_area','metric_id_type','entity','metric_id','dims','Missing_month']]
            df_missing_records =pd.DataFrame()
            df_missing_records=df_lifetime.append(df_monthly)
           
            # print(df_lifetime)
            # df_lifetime.to_csv(f'missing_record.csv',sep='|',index=False)

            df_missing_records['entity']=df_missing_records['entity'].astype(int)
            df_missing_records['metric_id']=df_missing_records['metric_id'].astype(int)
    
            # if not(df_missing_records.empty):
            #     df_missing_records=self.remove_validated_records(df_missing_records)
            # df_missing_records.to_csv('lifetime_missing_record_test.csv',sep='|',index=False)
            
            # df_missing_records.to_csv(f'csv_files/missing_record_2.csv',sep='|',index=False)
        
               
            
            validation_result =self.validate_records(dates,connection,functional_area,manual_run_specs)
            # validation_result.to_csv("result1.csv",sep="|" ,index =False)
            validation_result =validation_result[validation_result['validation_result']=='DANGER']
            validation_result =validation_result[['metric_id','dims','entity','functional_area','metric_id_type','month_ending','metric_value']]
            
            df_missing_records,validation_result=self.remove_validated_records(df_missing_records,validation_result)
            # # # # validation_result = pd.read_csv("result.csv",sep="|" )
            # validation_result=pd.read_excel(f'csv_files/{functional_area}_validation.xlsx',sheet_name='outliers')
            # month_list =[reporting_end_period[0:7]]
            # validation_result =validation_result[validation_result['month_ending'].isin(month_list)]
            validation_result.to_csv(f"test_outliers.csv",sep="|" ,index =False)
            
            
            df_lvl_1 =df_lvl_1[['entity','met_cnt','metric_id']]
            

            
            # files_name=[f"{functional_area}_outliers.csv",f'{functional_area}_missing_record.csv']
            writer = pd.ExcelWriter(f'csv_files/{functional_area}_validation.xlsx', engine ='xlsxwriter')
            df_missing_records.to_excel(writer, sheet_name ='missing_records',index =False)
            validation_result.to_excel(writer, sheet_name ='outliers',index =False)
            writer.save()
            
            # receivers_email=["abhinavkumar1243@gmail.com","parvez.hussain@wittybrains.com"]
            receivers_email=["abhinavk1268@gmail.com"]
            # self.send_mail(receivers_email,f'{functional_area}_validation',subject=f'validation - {functional_area}',functional_area =functional_area,files_name=[f'csv_files/{functional_area}_validation.xlsx'],html_template='mail',df_list=[validation_result,df_missing_records],description=f'Validation results for functional_area : {functional_area}')
            """
            connection.close()
                        
        except Exception as  exception:
           self.logger.error(f'Exception  arise as : {exception}')
           raise exception
        
if __name__ == '__main__':
    import time 
    starttime =time.time()
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
        validation=Kpi_qbr_validation()
        validation.main(reporting_end_period,no_of_months,manual_run_specs,functional_area=functional_area)
        execution_time =time.time()-starttime
        validation.logger.info(f'successfully executed......in {execution_time} sec')
    except Exception as exception:
        validation.logger.error(f'Exception arise as {exception}')




    