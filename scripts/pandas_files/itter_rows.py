import pandas as pd 

def get_tuple_list(df):
   list_tup=[]
   for i in df.itertuples(index=False):
      list_tup.append(tuple(i))
   return list_tup
   
