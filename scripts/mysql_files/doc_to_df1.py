from cmath import polar
from dataclasses import dataclass
from typing import DefaultDict
import pandas as pd
import numpy as np 
import pymongo
from ast import literal_eval
from lib import read_config

from lib.transform import drop_col

myclient = pymongo.MongoClient("mongodb://localhost:27017/")


def col_append_string(df, args):
    col_initial = args[0]
    value = args[1]
    delimiter = args[2]
    df[col_initial] = df.apply(lambda x: '{}{}{}'.format(x[col_initial], delimiter, value), axis=1)
    return df

def col_combine(df, args):
    col_initial = args[0]
    col_second = args[1]
    delimiter = args[2]
    df[col_initial] = df.apply(lambda x: '{}{}{}'.format(x[col_initial], delimiter, x[col_second]), axis=1)
    return df

def col_melt_from_list(df, args):
    id_vars_col = list(df.columns)
    value_vars_col = []
    to_melt_col = args[0].split(',')
    for col in to_melt_col:
        if col in id_vars_col:
            id_vars_col.remove(col)
            value_vars_col.append(col)
    df = pd.melt(df, id_vars=id_vars_col, value_vars=value_vars_col, var_name=args[1], value_name=args[2])
    return df

def explode_column(df, args):
    df = df.explode(args[0]).reset_index(drop=True)
    return df

def col_set(df, args):
    df[args[0]]= args[1]
    return df

def col_drop(df, args):
    return df.drop(args[0], axis = 1)

def col_rename(df, args):
    if (args[0] in list(df.columns)):
        df = df.rename(columns= {args[0]:args[1]}, errors="raise")
    return df

def col_split_by(df, args):
    col_initial = args[0]
    mid_cols = args[1].split(',')
    split_delimiter = args[-1]
    if col_initial in list(df.columns):
        df[mid_cols] = df[col_initial].str.split(split_delimiter, expand=True)
    return df

def flatten_column(df, args):
    # convert dtype to object if entire columns is NaN(float type) 
    if df[args[0]].dtype == 'float':
        print("in if ")
    
        df[args[0]] = df[args[0]].astype('object')

    # filling null values with {}
    for row in df.loc[df[args[0]].isnull(), args[0]].index:
        df.at[row, args[0]] = {}

    df_new = pd.json_normalize(df[args[0]])
   
    # get new columns names if provided
    if len(args) > 1:
        columns={}
        for x in args[1:]:
            names=x.split(':')
            columns[names[0]]=names[1]
        
        for column in columns.keys() :
            # create column and put value as None if column name provided doesn't exist
            if column not in df_new.columns.tolist():
                df_new[column]=None

        df_new = df_new.rename(columns=columns, errors="raise")

    return pd.concat([df,df_new], axis=1)

def main():
    
    db = myclient["test_db"]
    collection = db["product"]
    mongo_docs=[]
    documents = collection.find({},{"_id":0})
    for document in documents:
        mongo_docs.append(document)
    
    df = pd.json_normalize(mongo_docs)
    # df = col_rename(df,["product.0.Price","prod_price"])
   
    df = explode_column(df,["Customer"])
    df = flatten_column(df,["Customer","first_name:First_name","last_name:Last_name","email:email:","gender:gender","address:address"])
    df = col_drop(df, ["Customer"])
    
    df = explode_column(df,["product"])
    df = flatten_column(df,["product","stock_industry:stock_industary","department:Department",])
    df = drop_col(df,["product"])
    
    df = explode_column(df,["address"])
    df = flatten_column(df,["address"])
    df = drop_col(df,["address"])
    df['Name'] = df[['First_name','Last_name']].apply(lambda x: ' '.join(x), axis = 1)
    df = df['Name'].drop_duplicates()
    # df =df["email"].drop_duplicates()
    print(list(df))
    # df.to_csv("product.csv",sep="|",index=False)
    
if __name__ == "__main__":
    # main()
    from datetime import datetime
    pool_cnxn=read_config.mysl_pool_connection("mysql_web_data")
    mycursor=pool_cnxn.cursor()
    
    time_now = datetime.now()
    val = [(5,11,time_now,True,True,"scale",'1011'),(6,12,time_now,True,True,"scale",'1012'),(14,13,time_now,True,True,"scale",'1013'),
           (15,14,time_now,True,True,"scale",'1014'),(23,15,time_now,True,True,"scale",'1016'),(24,16,time_now,True,True,"scale",'1015')]
    
    query = "insert into web_data.scaleback_redemption_codes (redemption_code,sso_id,assigned_date,assigned, sent_to_fitbit, code_type,customer) values (%s,%s,%s,%s,%s,%s,%s)"
    
    mycursor.executemany(query,val)
    pool_cnxn.commit()
    # query = " select * from web_data.scaleback_redemption_codes"
    # df = pd.read_sql(sql = query,con= pool_cnxn)
    # print(df)