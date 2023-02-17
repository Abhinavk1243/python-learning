import json
import pandas as pd
import re
f=open(f"qbr_json_final_new.json",)
list_dict=json.load(f)
f1=open(f"json1.json",)
old_json=json.load(f1)
data_query=[]
metric_ids = []

df = pd.DataFrame(list_dict)
df_new=df[["slide_title","visualization_name","data_query"]]
# print(df_new)

df1 = pd.DataFrame(old_json)
df_old=df1[["slide_title","visualization_name","data_query"]]
# print(df_old)

df_old =df_old.rename(columns = {'data_query':'old_data_query'})
# print(df_old)

df_merge = pd.merge(df_new, df_old, on=["slide_title","visualization_name"], how='outer')
# print(df_merge)


writer = pd.ExcelWriter('C:/Users/Abhinav.kumar/Desktop/GIT/all_entity_test.xlsx', engine ='xlsxwriter')
df_merge.to_excel(writer, sheet_name ='json',index =False)
writer.save()