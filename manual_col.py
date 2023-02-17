from operator import index
from urllib.parse import _NetlocResultMixinStr
import pandas as pd 
import numpy as np
from sqlalchemy import create_engine, null

# # validation_result = pd.read_excel('validation_met.xlsx', sheet_name='validation_result')
# validation_result_monthly = pd.read_excel('qbr_incentives_validation.xlsx', sheet_name='outliers')
# SQLALCHEMY_DATABASE_URI='mysql://root:abhinav12@127.0.0.1:3306/test_db?charset=utf8'

# engine = create_engine(SQLALCHEMY_DATABASE_URI)

# # validation_result.to_sql('validation_result',engine, if_exists= 'replace',index=False)
# validation_result_monthly.to_sql('outliers',engine, if_exists= 'replace',index=False)
# import seaborn as sns
list_1 =[1.0, 56.0, 150.0, 151.0, 159.0, 181.0, 196.0, 235.0, 264.0, 267.0, 295.0, 634.0, 718.0, 960.0, 980.0]
# a=sns.boxplot(list_1)
# fig = a.get_figure()
# fig.savefig('svm_conf.png', dpi=400)
# print(a)

from scipy import stats
import numpy as np
 
z = np.abs(stats.zscore(list_1))
print(np.where(z > 3))














# 
# # data =  {'Name':['Jai', 'Princi', 'Gaurav', 'Anuj'], 
# #         'Age':[27, 24, 22, 32], 
# #         'Address':['Nagpur', 'Kanpur', 'Allahabad', 'Kannuaj'], 
# #         'Qualification':['Msc', 'MA', 'MCA', 'Phd'],
# #         'Mobile No': [97, 91, 58, 76]} 

# # df = pd.DataFrame(data)
# # print(df)

# table_old = 'enr_old'
# table_new = 'enrolls_new'
# df_old.to_sql('coaching',engine, if_exists= 'replace',index=False)
# df_new.to_sql('coaching',engine, if_exists= 'replace',index=False)

# # df = pd.read_sql_table('old_metadata',engine)
# # print(df)


# sql = '''select distinct * from (
# SELECT case 
#         when n.metric_id is null then o.metric_id
#         when o.metric_id is null then n.metric_id
#         else o.metric_id 
#     end as metric_id,
#     o.reportgroupname as old_reportgroupname,
#         n.reportgroupname as new_reportgroupname,
#         o.dims as old_dims,
#         n.dims as new_dims,
#         o.metric as old_cnt,
#         n.metric as new_cnt FROM test_db.enrolls_old o 
# LEFT JOIN test_db.enrolls_new  n ON (o.reportgroupname = n.reportgroupname and o.metric_id =n.metric_id and o.dims = n.dims)
# UNION
# SELECT case 
#         when n.metric_id is null then o.metric_id
#         when o.metric_id is null then n.metric_id
#         else o.metric_id 
#     end as metric_id,
#     o.reportgroupname as old_reportgroupname,
#         n.reportgroupname as new_reportgroupname,
#         o.dims as old_dims,
#         n.dims as new_dims,
#         o.metric as old_cnt,
#         n.metric as new_cnt FROM test_db.enrolls_old o
# RIGHT JOIN test_db.enrolls_new  n ON (o.reportgroupname = n.reportgroupname and o.metric_id =n.metric_id and o.dims = n.dims)
# ) as a
# order by 1,2,3,4,5'''

# writer = pd.ExcelWriter('enrolls.xlsx', engine ='xlsxwriter')
# sql ='SELECT * FROM test_db.site_analytics_new where reportgroupid =53750005'
# df = pd.read_sql(sql=sql ,con=engine)
# df['new_cnt'] = df['new_cnt'].replace(to_replace='(null)',value='0')
# df['old_cnt'] = df['old_cnt'].replace(to_replace='(null)',value='0')
# df['old_cnt']= df['old_cnt'].fillna(0)
# df['new_cnt']= df['new_cnt'].fillna(0)
# df['new_cnt'] =df['new_cnt'].astype(float)
# df['old_cnt'] =df['old_cnt'].astype(float)
# df['count-difference(old-new)'] = df['old_cnt']-df['new_cnt']
# df.to_excel(writer, sheet_name ='enrolls-allreportgroups',index =False)
# # writer.save()

# df['old_reportgroupname'] = df['old_reportgroupname'].fillna(value=np.nan)
# df['new_reportgroupname'] = df['new_reportgroupname'].fillna(value=np.nan)
# df['old_reportgroupname']= df['old_reportgroupname'].fillna(0)
# df['new_reportgroupname']= df['new_reportgroupname'].fillna(0)
# df = df[df['old_reportgroupname'] !=0 ]
# df = df[df['new_reportgroupname'] !=0 ]
# # print(df)
# list1 = ['metric_id','old_reportgroupname','new_reportgroupname','old_dims','new_dims']
# df = df.drop_duplicates(subset=list1,keep= 'last')
# df.to_excel(writer, sheet_name ='enrolls-common-reportgroups',index =False)
# writer.save()

