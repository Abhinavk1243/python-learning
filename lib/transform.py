import pandas as pd
from lib import read_config
logger=read_config.logger()

def col_rename(df,old_col_name,new_col_name):
    df.rename(columns = {old_col_name: new_col_name }, inplace = True)
    return df


def col_filter_unspecified(df,col_name):
    df=df[df[col_name] !="::unspecified::"]
    return df

"""def col_filter_zero(df):
    df=pd.melt(df,id_vars=["datetime","datetime_friendly","prop28","prop31","prop16","prop8"],var_name="metric_name",value_name="metric_value")
    df["metric_value"]=df["metric_value"].astype(int)
    df=df[df.metric_value>0]
    return df
"""
