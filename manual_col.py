from urllib.parse import _NetlocResultMixinStr
import pandas as pd 
import numpy as np
from py import test
df = pd.read_excel('manual_cols.xlsx', sheet_name='Sheet2')
all_column = list(df["All Columns"].apply(lambda x: x.strip()))
all_post_dup_col = list((df['Columns whose "post_" suffix are available']).dropna().apply(lambda x: str(x).strip()))
adobe_null =list((df['Not Needed Columns (Reported By Adobe)']).dropna().apply(lambda x: str(x).strip()))
no_longer_use =list((df['No longer used (Adobe)']).dropna().apply(lambda x: str(x).strip()))
post_not_needed = list((df['post_not_needed']).dropna().apply(lambda x: str(x).strip()))
post_no_longer_use = list((df['post_no_longer_used']).dropna().apply(lambda x: str(x).strip()))
# print(df)
total_no_use = all_post_dup_col + adobe_null + no_longer_use  + post_not_needed + post_no_longer_use
# post_not_needed = [f"post_{i}" for i in no_longer_use if i in all_post_dup_col]

final_col = [i for i in all_column if i not in total_no_use]

for i in final_col:
      print(i)













# final_cols = list(df["Final (removing post_ dups)  (Col C - Col D)"].apply(lambda x: str(x).strip()))
# distinct = list(df["Cols_after_removing_distinct_cols_from_all_columns"].apply(lambda x: str(x).strip()))

# list_1 = [i for i in final_cols if i not in distinct ]

# for i in list_1:
#       print(i)

# def remove_dup(test_list):
#       res = []
#       for i in test_list:
#             if i not in res:
#                   res.append(i)
      
#       return res
# # Columns whose "post_" suffix are available

# all_column = list(df["All Columns"].apply(lambda x: x.strip()))
# adobe_null_col = list((df["Not Needed Columns (Reported By Adobe)"]).dropna().apply(lambda x: str(x).strip()))
# col_post =list((df['Columns whose "post_" suffix are available']).dropna().apply(lambda x: str(x).strip()))
# no_longer_use =list((df['No longer used (Adobe)']).dropna().apply(lambda x: str(x).strip()))
# col_after_remove_post = [i for i in all_column if i not in col_post]
# post_not_needed = [f"post_{i}" for i in adobe_null_col]
# col_after_not_needed_post = [i for i in col_after_remove_post if i not in post_not_needed]
# # print(len(col_after_not_needed_post))
# cols_after_remove_not_needed = [i for i in col_after_not_needed_post if i not in adobe_null_col]

# col_value_null_as_feb = list((df['Column values as null (data_feed_external_feb)']).dropna().apply(lambda x: str(x).strip()))


# total_cols = adobe_null_col + col_post + no_longer_use
# total_cols = remove_dup(total_cols)

# cols_removing_total = [i for i in all_column if i not in total_cols]
# for i in cols_removing_total:
#       print(i)
# print(len(total_cols))
# for i in total_cols:
#       print(i)
# for i in col_value_null_as_feb:
#       print(i)
# col_value_null_remove_no_longer_use = [i for i in col_value_null_as_feb if i not in no_longer_use]
# for i in col_value_null_remove_no_longer_use:
#       print(i)
# final_cols = [i for i in cols_after_remove_not_needed if i not in no_longer_use]
# for i in col_value_null_remove_no_longer_use:
#       print(i)
      
# print(len(col_post))
# adobe_null_col = adobe_null_col.where(pd.notnull(df), None)
# print(df.columns)
# post_suffix_available_cols=list(df["post_ suffix available cols"].apply(lambda x: str(x).strip()))
# columns_after_removing_not_needed= list(df["Columns after Removing Not Needed"].apply(lambda x: str(x).strip()))
# columns_after_removing_post_not_needed = list(df["Columns after removing post_ Not Needed"].apply(lambda x: str(x).strip()))

# not_needed_post_cols = [f"post_{i}" for i in post_suffix_available_cols if i in adobe_null_col if i is not np.nan ]

# columns_after_removing_not_needed_prog= [i for i in all_column if i not in adobe_null_col ]
# columns_after_removing_post_not_needed_prog =[i for i in columns_after_removing_not_needed_prog if i not in not_needed_post_cols ]
# final_column =  [i for i in columns_after_removing_post_not_needed if i not in post_suffix_available_cols ]




# data={
#       "columns_after_removing_post_not_needed_prog":columns_after_removing_post_not_needed_prog,
#       }

# df_1 = pd.DataFrame(data)
# file_name = "adobe_data_feed.xlsx"
# key = "programing_Columns"
# df_1.to_excel(file_name, sheet_name=key,index=False)
# print
# df["All Columns"] ="pageview"
# print(df)