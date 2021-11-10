import pandas as pd
from lib import read_config
# logger=read_config.logger()

def col_rename(df,args):
    try:
        df.rename(columns = {args[0]: args[1]}, inplace = True)
        # logger.debug(f"column rename from {args[0]} to {args[1]} ")
        return df
    except Exception as error:
        
        return df
    # return df

def col_rename_index(list_df,args):
    index = int(args[2])
    old_name = args[0]
    new_name = args[1]
    list_df[index].rename(columns = {old_name: new_name}, inplace = True)
    return list_df

def col_filter_unspecified(df,args):
    try:
        col=args[0]
        df=df[df[col] != '::unspecified::']
        # logger.debug(f" {args[0]} where value = ::unspecified::")
        
        return df
    except Exception  as error:
        
        return error

def col_melt(df,args):
    try:
        args[0]=args[0].split(",")
        if args[1]=="None":
            df=pd.melt(df,id_vars=args[0],var_name=args[2],value_name=args[3])
            
        return df
    except Exception as error:
        
        return error

def col_filter_zero(df,args):
    try:
        df[args[0]]=df[args[0]].astype(int)
        df=df[df[args[0]]>0]
        # logger.debug(f"dataframe melt and filer row {args[0]} where value = 0 ")
        return df
    except Exception as error:
        
        print(f"error arise as : {error}") 

def col_drop(df,args):
    try:
        df.drop([args[0]], axis = 1,inplace = True)
        return df
    except Exception as error:
        print(f"Error arise as {error}")
        

def col_filter_none(df,args):
    try:
        df=df[df[args[0]] !="none"]
        # logger.debug(f" {args[0]} where value = 0 ")
        return df
    except Exception  as error:
        
        return error
    
def string_strip(df,args):
    df[args[0]]=df[args[0]].str.strip(args[1])
    return df

def string_replace(df,args):
    df[args[0]]=df[args[0]].str.replace(args[1],args[2])
    return df

def get_date(df,args):
    date = args[0]
    # hour =args[1]
    # minute = args[2]
    # df[date] = df[date].str.cat(df[hour], sep ="")
    # df[date] = df[date].str.cat(df[minute], sep ="")
    df[date]= pd.to_datetime(df[date]) 
    df[date]=df[date].dt.strftime('%d-%b-%Y (%H:%M)')
    return df

def drop_col(df,args):
    for col in args:
        del df[col]
        
    return df