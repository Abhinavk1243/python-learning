from mysql.connector.pooling import generate_pool_name
from numpy.core.records import record
from lib import read_config
from datetime import date
import pandas as pd
import numpy as np

from lib.jsonfile import read_json_file
pool_cnxn =  read_config.mysl_pool_connection("mysql")
mycursor = pool_cnxn.cursor()

def calc_df(df_vertica,feature_col,output_col):
    df_vertica.columns = feature_col
    df_vertica = df_vertica.reindex(columns = output_col)
    df_vertica = df_vertica.transpose()
    df_vertica.columns = ['data']
    print(df_vertica)

def generate_report(record,feature_col,web_order,app_order):
    df_vertica_web = pd.DataFrame()
    df_vertica_app = pd.DataFrame()
    
    for row in record:
        if row[1]=="Web":
            df_vertica_web = pd.DataFrame(row)[2:].transpose()
        elif row[1] == 'App':
            df_vertica_app = pd.DataFrame(row)[2:].transpose()
            
    # 
    print("APP")
    
    calc_df(df_vertica_app,feature_columns,app_order)
    print("WEB")
    
    calc_df(df_vertica_web,feature_columns,web_order)
    
    
   
    
    # print(df_vertica_web)
            
    
def main(col_list):
    start_date = '2021-12-20'
    query_feature = f"""select date,(CASE WHEN platform IN ('iOS','Android') THEN 'App' else 'Web' END) AS platform 
          ,
          sum(case when feature = 'FAD' AND metric_name = 'Visits' then metric_value else 0 end) as FAD_Visits,
          sum(case when feature = 'AskMD' AND metric_name = 'Visits' then metric_value else 0 end) as AskMD_Visit
           from test_db.feature
        where date = "{start_date}"
        group by date,(CASE WHEN platform IN ('iOS','Android') THEN 'App' else 'Web' END) 
        order by date,platform;"""
    
    query_user = f"""select date,(CASE WHEN platform IN ('iOS','Android') THEN 'App' else 'Web' END) AS platform 
          
          ,sum(case when metric_name = 'FAD Visits' then metric_value else 0 end) as FAD_Visits
        ,sum(case when metric_name = 'AskMD Visits' then metric_value else 0 end) as AskMD_Visits
        ,sum(case when metric_name = 'Content Pins' then metric_value else 0 end) as Content_Pins
           from test_db.adobe_user
        where date = "{start_date}"
        group by date,(CASE WHEN platform IN ('iOS','Android') THEN 'App' else 'Web' END) 
        order by date,platform;
    """
    # query = query_feature
    query = query_user
    df = pd.read_sql(sql=query,con = pool_cnxn)
    # print(df)
    print(df.shape[0])
    # mycursor.execute(query)
    # record = mycursor.fetchall()
    # generate_report(record,col_list[0],col_list[1],col_list[2])
  
    # print(mycursor.fetchall()
    # query = "insert into test_db.adobe_user (date, user_id, platform, metric_name, metric_value) values(%s,%s,%s,%s,%s)"
    # date1 = "2021-12-20"
    # val = [(date1,1 ,"Web","AskMD Visits",2),(date1,2,"Web","FAD Visits",3),(date1,3 ,"Web","FAD Visits",5)
    #        ,(date1,4 ,"Web","Content Pins",5),(date1,5,"Android","Content Pins",1),
    #        (date1,6,"Android","AskMD Visits",3),(date1,7 ,"iOS","Content Pins",5),
    #        (date1,8 ,"iOS","AskMD Visits",1)]
    # mycursor.executemany(query,val)
    # pool_cnxn.commit()
    # print("insert")
    
if __name__ == "__main__":
    # feature_columns = [
    #         'FAD_Visits','AskMD_Visits','Content_Pins'
    #     ]
    # app_order = [
    #     'AskMD_Visits','Content_Pins'
    #     ]
    # web_order = [
    #         'FAD_Visits','AskMD_Visits','Content_Pins'
    #     ]
    # list_1 = [feature_columns,web_order,app_order]
    # # main(list_1)
    # import requests
    
    # emp = read_json_file("employe")
    # print(emp)
    # df = pd.DataFrame().from_dict(emp)
    # # # df = df.drop_duplicates(subset=["userId"])
    # print(df)
    
    list_1 = [('242,100,124,132,133,149,500,501,502,503'),
            ('203,100,122,124,132,133,150,157,162,179'),
            ('20178,122,124,133,150,157,162,179,500,501,502,503'),
            ('203,100,104,122,124,132,133,150,162,163,179'),
            ('287,104,122,124,150,162,179'),
            ('20426,100,104,122,124,132,133,144,150,162,176,179,500,501,502,503'),
            ('216,104,108,116,122,124,132,133,150,162,179'),
            ('203,100,104,122,124,132,133,150,162,163,179'),
            ('20106,104,117,122,124,133,162,179'),
            ('20107,104,117,122,124,133,162,179,500,501,502,503'),
            ('20137,100,104,122,124,144,145,146,147,148,150,152,162,169,179'),
            ('20137,100,104,122,124,144,145,146,147,148,150,152,162,169,179'),
            ('20137,100,104,122,124,144,145,146,147,148,150,152,162,169,179'),
            ('20137,100,104,122,124,144,145,146,147,148,150,152,162,169,179'),
            ('20137,100,104,122,124,144,145,146,147,148,150,152,162,169,179'),
            ('20137,100,104,122,124,144,145,146,147,148,150,152,162,169,179'),
            ('20137,100,104,122,124,144,145,146,147,148,150,152,162,169,179'),
            ('20137,100,104,122,124,144,145,146,147,148,150,152,162,169,179'),
            ('20137,100,104,122,124,144,145,146,147,148,150,152,162,169,179'),
            ('20137,100,104,122,124,144,145,146,147,148,150,152,162,169,179'),
            ('20137,100,104,122,124,144,145,146,147,148,150,152,162,169,179'),
            ('20137,100,104,122,124,144,145,146,147,148,150,152,162,169,179'),
            ('20137,100,104,122,124,144,145,146,147,148,150,152,162,169,179'),
            ('20137,100,104,122,124,144,145,146,147,148,150,152,162,169,179'),
            ('20137,100,104,122,124,144,145,146,147,148,150,152,162,169,179'),
            ('20137,100,104,122,124,144,145,146,147,148,150,152,162,169,179'),
            ('203,100,104,122,124,132,133,150,160,162,163,179,500,501,502,503'),
            ('203,244,100,104,122,124,132,133,150,160,162,179,500,501,502,503'),
            ('245,297,293,203,100,104,122,124,132,133,150,160,179,500,501,502,503'),
            ('203,100,104,122,124,132,133,150,160,162,163,179')]
    
    
    # query = 'insert into web_data.data_feed_external_jan  values(%s)'
    # mycursor.executemany(query,list_1)
    # pool_cnxn.commit()
    
    # l =0 
    # for i in list_1:
    #     l = l +len(i)
        
    # print(l)
    import pandas as pd
    import os
    import numpy as np
    import openpyxl 
    df = pd.read_csv("col_feb.csv")
    # print(df['mobilecampaigncontent'])
    data_dict = df.to_dict(orient="records")
    # print(data_dict)
    keep_col=[]
    remove_col = []
    
    for i,j in data_dict[0].items():
        if j=="Keep":
            keep_col.append(i)
        elif j=="Remove":
            remove_col.append(i)
    
    # print(df["mobilecampaigncontent"])
    # col_reports=["mobileacquisitionclicks","mobileactioninapptime","mobileactiontotaltime","mobileappperformanceaffectedusers","mobileappperformanceappid.app-perf-app-name","mobileappperformanceappid.app-perf-platform","mobileappperformancecrashes","mobileappperformancecrashid.app-perf-crash-name","mobileappperformanceloads","mobileappstoreavgrating","mobileappstoredownloads","mobileappstoreinapprevenue","mobileappstoreinapproyalties","mobileappstoreobjectid.app-store-user","mobileappstoreobjectid.application-name","mobileappstoreobjectid.application-version","mobileappstoreobjectid.appstore-name","mobileappstoreobjectid.category-name","mobileappstoreobjectid.country-name","mobileappstoreobjectid.device-manufacturer","mobileappstoreobjectid.device-name","mobileappstoreobjectid.in-app-name","mobileappstoreobjectid.platform-name-version","mobileappstoreobjectid.rank-category-type","mobileappstoreobjectid.region-name","mobileappstoreobjectid.review-comment","mobileappstoreobjectid.review-title","mobileappstoreoneoffrevenue","mobileappstoreoneoffroyalties","mobileappstorepurchases","mobileappstorerank","mobileappstorerankdivisor","mobileappstorerating","mobileappstoreratingdivisor","mobileavgprevsessionlength","mobilecrashes","mobilecrashrate","mobiledailyengagedusers","mobiledeeplinkid.name","mobileinstalls","mobilelaunches","mobileltvtotal","mobilemessageclicks","mobilemessageid.dest","mobilemessageid.name","mobilemessageid.type","mobilemessageimpressions","mobilemessagepushpayloadid.name","mobilemessageviews","mobilemonthlyengagedusers","mobileplacedwelltime","mobileplaceentry","mobileplaceexit","mobileprevsessionlength","mobilerelaunchcampaigntrackingcode.name","mobileupgrades","socialaveragesentiment","socialaveragesentiment (deprecated)","socialfbstories","socialfbstorytellers","socialinteractioncount","sociallikeadds","sociallink","sociallink (deprecated)","socialmentions","socialpageviews","socialpostviews","socialproperty","socialproperty (deprecated)","socialpubcomments","socialpubposts","socialpubrecommends","socialpubsubscribers","socialterm","socialtermslist","socialtermslist (deprecated)","socialtotalsentiment","sourceid","videoauthorized","videoaverageminuteaudience","videochaptercomplete","videochapterstart","videochaptertime","videopause","videopausecount","videopausetime","videoplay","videoprogress10","videoprogress25","videoprogress50","videoprogress75","videoprogress96","videoqoebitrateaverage","videoqoebitratechange","videoqoebuffer","videoqoedropbeforestart","videoqoedroppedframes","videoqoeerror","videoresume","videototaltime","videouniquetimeplayed"]
    df_1 = pd.DataFrame({'KEEP':keep_col})
    # df_1 = pd.DataFrame({'REMOVE':remove_col})
    
    file_name = "adobe_data_feed.xlsx"
    key = "columns_data_feed"
    df_1.to_excel(file_name, sheet_name=key,index=False)
    
    
  
    