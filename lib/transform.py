# import pandas as pd
# from lib import read_config
# import re

# def col_rename(df,args):
#     try:
#         df.rename(columns = {args[0]: args[1]}, inplace = True)
#         # logger.debug(f"column rename from {args[0]} to {args[1]} ")
#         return df
#     except Exception as error:
        
#         return df
#     # return df

# def col_rename_index(list_df,args):
#     index = int(args[2])
#     old_name = args[0]
#     new_name = args[1]
#     list_df[index].rename(columns = {old_name: new_name}, inplace = True)
#     return list_df

# def col_filter_unspecified(df,args):
#     try:
#         col=args[0]
#         df=df[df[col] != '::unspecified::']
#         # logger.debug(f" {args[0]} where value = ::unspecified::")
        
#         return df
#     except Exception  as error:
        
#         return error

# def col_melt(df,args):
#     try:
#         args[0]=args[0].split(",")
#         if args[1]=="None":
#             df=pd.melt(df,id_vars=args[0],var_name=args[2],value_name=args[3])
            
#         return df
#     except Exception as error:
        
#         return error

# def col_filter_zero(df,args):
#     try:
#         df[args[0]]=df[args[0]].astype(int)
#         df=df[df[args[0]]>0]
#         # logger.debug(f"dataframe melt and filer row {args[0]} where value = 0 ")
#         return df
#     except Exception as error:
        
#         print(f"error arise as : {error}") 

# def col_drop(df,args):
#     try:
#         df.drop([args[0]], axis = 1,inplace = True)
#         return df
#     except Exception as error:
#         print(f"Error arise as {error}")
        

# def col_filter_none(df,args):
#     try:
#         df=df[df[args[0]] !="none"]
#         # logger.debug(f" {args[0]} where value = 0 ")
#         return df
#     except Exception  as error:
        
#         return error
    
# def string_strip(df,args):
#     df[args[0]]=df[args[0]].str.strip(args[1])
#     return df

# def string_replace(df,args):
#     df[args[0]]=df[args[0]].str.replace(args[1],args[2])
#     return df

# def get_date(df,args):
#     date = args[0]
#     # hour =args[1]
#     # minute = args[2]
#     # df[date] = df[date].str.cat(df[hour], sep ="")
#     # df[date] = df[date].str.cat(df[minute], sep ="")
#     df[date]= pd.to_datetime(df[date]) 
#     df[date]=df[date].dt.strftime('%d-%b-%Y (%H:%M)')
#     return df

# def drop_col(df,args):
#     for col in args:
#         del df[col]
        
#     return df

# def col_split_into_list_by_value(df,args):
#     """split column oon based of  value

#     Args:
#         df (object): dataframe on which operation has to be performed
#         for examle args (array): [pagename|card_category,card_type,card_name_id|-]
#     """
    
#     # Insurance Card|standard|pageviews
#     col_initial = args[0]
#     final_col_list = args[1]
#     split_delimiter = args[2]
#     final_col_list = final_col_list.split(",")
#     # exp = ((df['pagename'].str.lower()).str.contains("standard")) & (df["metric_name"]=="pageviews")
#     exp=(df["metric_name"]=="pageviews")
    
#     meta_df = df[exp]
    
#     df = df[~exp]
    
#     df_new = pd.DataFrame(meta_df[col_initial].apply(split_cols_value_and_validate_length_input,delimeter=split_delimiter).tolist(),columns=final_col_list)
    
#     meta_df= meta_df.reset_index()
#     meta_df= pd.concat([meta_df, df_new],axis=1)
#     meta_df =meta_df.drop("index",axis=1)
#     meta_df.to_csv("pagename-csv-data/meta_df.csv",index = False,sep = "|")
#     df = df.append(meta_df)
    
#     return df

# def split_cols_value_and_validate_length_input(name,delimeter):
#     split_value = name.split(delimeter) 
#     split_value = [x.strip() for x in split_value]
    
    
#     all_char= "[0-9A-Za-z@_!#$%^&*()<>?/\|-}{~:+-=,.\s]*"
#     pattern = f"{all_char}health{all_char}wallet{all_char}card{all_char}detail{all_char}"
    
#     if re.search("standard",str(name).lower()):
#         input ="Insurance Card"
#         if len(split_value) == 3:
#             if split_value[2] == input:
#                 return ["",input,split_value[1].title()]
#             else:
#                 return ["",split_value[1].title(),split_value[2].title()]
#         elif len(split_value) == 4:
#             if split_value[3] == input:
#                 return ["",input,f"{split_value[1]} {split_value[2]}".title()]
#             else:
#                 return ["",f"{split_value[1]} {split_value[2]}".title(),split_value[3].title()]
                
#         elif len(split_value) == 5:
#             if split_value[4] == input:
#                 return ["",input,f"{split_value[1]} {split_value[2]} {split_value[3]}".title()]
#             else:
#                 return ["",f"{split_value[1]} {split_value[2]} {split_value[3]}".title(),split_value[4].title()]
        
#         else:
#             return ["","",""]
        
#     elif re.findall(pattern,str(name).lower()):
#         if len(split_value) == 3:
#             return ['Health Wallet Card Detail',"",split_value[2].title()]
#         elif len(split_value) ==4:
#             return ['Health Wallet Card Detail',"",f"{split_value[2]} {split_value[3]}".title()]
#         else:
#             return ["","",""]
        
#     else:
#         return ["","",""]

import re
import logging
import numpy as np
import pandas as pd
from datetime import datetime


def col_melt(df, args):
    """
    To melt the dataframe
    For ex : args = ['date,platform,userid,pagename,market','include','feature','metric_name']
    """

    id_vars = list(args[0].split(','))
    value_vars = (list(set(df.columns) - set(id_vars))) if (args[1] == 'include') else None
    var_name = args[2]
    value_name = args[3]

    if value_vars:
        df = df.melt(id_vars=id_vars,
                    value_vars=value_vars,
                    var_name=var_name,
                    value_name=value_name)
    else:
        df = df.melt(id_vars=id_vars,
                    var_name=var_name,
                    value_name=value_name)
    return df


def col_split_by(df, args):
    """
    To split the column into two columns by delimiter
    For ex : args = ['feature','metric_name','-']
    """
    col_initial = args[0]
    col_second = args[1]
    split_delimiter = args[2]
    if col_initial in list(df.columns):
        df[[col_initial, col_second]] = df[col_initial].str.split(split_delimiter, expand=True)
    return df


def col_add_index(df_list, args):
    """ 
    To add the the column at a particular dataframe present on indexs

    args[0]: The column to add
    args[1]: The value of column
    args[2]: The dataframe at positions (to split by ',') ex: col_add_index=>platform|Web|0,1
    """

    split_index = list(map(int, args[2].split(',')))
    for df_index in split_index:
        if df_index < len(df_list):
            df_list[df_index] = col_set(df=df_list[df_index], args=[args[0], args[1]])
    return df_list


def col_rename(df, args):
    """ 
    To rename the column of dataframe 

    args[0]: existing column name
    args[1]: new column name
    """
    if (args[0] in list(df.columns)):
        df = df.rename(columns= {args[0]:args[1]}, errors="raise")
    return df


def col_reindex(df, args):
    """ 
    To reindex/re-arrange the columns of dataframe 

    args: existing column name
    """
    final_columns = args
    df = df.reindex(columns = final_columns)
    return df


def col_filter_zero(df, args):
    """ Filter all rows where column args[0] > 0 """
    df = df[df[args[0]] > 0]
    return df


def add_col_prefix(df, args):
    """
    Add the prefix to column names

    args[0]: prefix to be added to column names
    agrs[1:]: column names
    """
    prefix = args[0]
    columns = {}
    for col in args[1:]:
        columns[col] = f"{prefix}:{col}"
    return df.rename(columns = columns, errors="raise")


def date_from_millis(df, args):
    """ Convert column with epoch in milliseconds to datetime in EST"""
    df[args[0]] = pd.to_datetime(df[args[0]], unit='ms').dt.tz_localize('GMT')
    df[args[0]] = df[args[0]].dt.tz_convert('America/New_York')
    if len(args) == 1:
        df[args[0]]=df[args[0]].dt.strftime("%Y-%m-%d %H:%M:%S")
    else:
        df[args[0]]=df[args[0]].dt.strftime(args[1])
    return df


def col_to_timestamp(df, args):
    """ Convert column to datetime """

    df[args[0]] = pd.to_datetime(df[args[0]], format="%Y-%m-%d %H:%M:%S")
    return df


def col_to_est_timestamp(df, args):
    """ Convert datetime/datetime string column to EST timestamp """

    df[args[0]] = pd.to_datetime
    try:
        df[args[0]] = df[args[0]].dt.tz_localize('GMT')
        df[args[0]] = df[args[0]].dt.tz_convert('America/New_York')
    except:
        df[args[0]] = df[args[0]].dt.tz_convert('America/New_York')
    finally:
        if len(args) == 1:
            df[args[0]]=df[args[0]].dt.strftime("%Y-%m-%d %H:%M:%S")
        else:
            df[args[0]]=df[args[0]].dt.strftime(args[1])
    return df


def col_to_null(df, args):
    """ All column values to null """
    df[args[0]] = None
    return df


def col_change_int(df, args):
    """
    Change datatype of column to int

    args[0]: name of column to be converted to int
    """
    df[args[0]] = df[args[0]].astype(int)
    return df


def col_drop(df, args):
    """
    Drop a column from dataframe

    args[0]: name of column to be dropped
    """
    if args[0] in list(df.columns):
        df = df.drop(args[0], axis = 1)
    return df


def drop_multiple_columns(df, args):
    """
    Drop multiple columns from dataframe

    args: list of columns to be dropped
    """
    return df.drop(args, axis=1)


def col_date_format(df, args):
    """
    Converts a Date type column to a string type column. The format of the 
    string is specified by args[1]
    rule: col_date_format=>col_name|format  sample format "yyyy-MM-dd"

    arg[0]: name of column to be converted from Date type to String
    arg[1]: The Date to string conversion is specified by this argument
    """

    df[args[0]] = df[args[0]].dt.strftime(args[1])
    return df


def col_to_date(df, args):
    """ Convert column values from datetime to date"""
    df[args[0]] = pd.to_datetime(df[args[0]]).dt.date
    return df


def col_to_hour(df, args):
    """ Convert column values from datetime to hour"""
    df[args[0]] = pd.to_datetime(df[args[0]]).dt.hour
    return df


def col_set(df, args):
    """
    col_set=>col_name|col_value
    args[0]: column name
    args[1]: value
    Set rows in column args[0] to the value args[1].
    If column args[0] does not exit, create column and set rows of created column to args[1]
    """
    df[args[0]] = args[1]
    return df


def col_copy(df, args): # done
    """
    Copy col values from source column args[0] to destination column args[1]
    transformation rule: col_copy=>from_col|to_col
    args[0]: source column from_col
    args[1]: destination column to_col
    """
    df[args[1]] = df[args[0]]
    return df


def date_col_copy(df, args):
    df[args[1]] = pd.to_datetime(df[args[0]]).dt.strftime(args[2])
    return df


def add_date_col(df, args):
    """
    Add a date column. The column added is a Date type column
    rule: col_add_date=>col_name|today
    df: dataframe
    args[0]: name of new column where date inserted
    args[1]: date to add 'today' - add date returned by python function datetime.today()
    """
    dateOption2 = ''
    dateOption2 = args[1]
    if dateOption2.upper == 'TODAY':
        today = datetime.datetime.today()
        aDate = today.date()
    else:
        today = datetime.datetime.today()
        aDate = today.date()
        
    df[args[0]]= pd.to_datetime(aDate)
    return df


def col_change_type(df, args):
    """
    Change column type
    rule sample: col_change_type=>col_name|integer
    df: data frame
    args[0]: name of column to change type
    args[1]: type to change to. 'integer', 'float', 'string'
    """
    df[args[0]] = df[args[0]].astype(args[1])
    return df


def col_lower(df, args):
    """
    Converts values in column to lower case
    """
    df[args[0]] = df[args[0]].str.lower()
    return df


def rename_column_snake_case(df, args):
    new_name = re.sub('([A-Z]+)', r'_\1', args[0]).lower()
    df.rename(columns = {args[0]:new_name}, inplace = True)
    return df


def col_restructure(df, args):
    df[args[0]] = df[args[0]].astype(args[1])
    return df


def dp_timestamp(df, args = None):
    df["dp_timestamp"] = pd.datetime.utcnow()
    return df


def filter_selectcolumns(df, args):
    return df[args]


def flatten_column(df, args):
    # fill null values
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

def explode_column(df, args):
    df = df.explode(args[0]).reset_index(drop=True)
    return df

def col_regex_filter(df, args):
    """
    col_filter_regex=>[ACTION]|[column_name]|regex
    This transformer will SELECT or DELETE rows from a dataframe when the value of a column matches a regular expression. 
    Samples:             0       1         2
    col_filter_regex=>DELETE|code_name|^[0-9]+$
    Delete rows from data frame where column 'code_name' has all numeric numeric string.

    col_filter_regex=>SELECT|ssn|^\d{3}-\d{2}-\d{4}$
    SELECT rows in data frame where column 'ssn' matches social security number regex.
    """
    action = args[0].upper()
    col = args[1]
    
    array_regex = args[2:]
    item_count = len(array_regex)
    tmpstr=''
    n=0
    for item in array_regex:
        n=n+1
        if n == item_count:
            tmpstr = tmpstr + item
        else:
            tmpstr = tmpstr + item + '|'
    regex = tmpstr
    # print(f'regex: {regex}')
    
    if action == 'SELECT':
        df = df[df[col].str.contains(regex)].reset_index(drop=True)
    elif action in ['DEL', 'DELETE']:
        df = df[~df[col].str.contains(regex)].reset_index(drop=True)
    
    return df


def flatten_list_to_string(df, args):
    """
    Flatten list to a single string seperated by ':'
    ex: [a,b,c] => a:b:c

    args: column which has lists to be converted to string
    """

    col = args[0]
    df[col] = df[col].str.join(':')

    return df


def apply_regex(df, args):
    """
    Filter string to select only ascii values

    args[0]: column
    args[1]: regex string to apply ex: ([a-zA-Z0-9 ]+)
    """

    col = args[0]
    df[col] = df[col].str.extract(args[1])

    return df


def limit_string_length(df, args):
    """
    Cut strings to max length provided

    args[0]: column
    args[1]: max length
    """

    col = args[0]

    # check if entire columns is not null
    if not df[col].isnull().all():
        df[col] = df[col].str.slice(stop=args[1])

    return df


def replace_string(df, args):
    """
    Replace a sub string inside a string with provided string
    
    args[0]: column
    args[1]: string to be replaced
    args[2]: new replacement string
    """
    col = args[0]
    ## Check if entire columns is not null
    if not df[col].isnull().all():
        df[col] = df[col].str.replace(args[1], args[2])
    return df


def strip_string(df, args):
    """
    Strip whitespaces (including newlines)

    args[0]: column
    """

    col = args[0]

    # check if entire columns is not null
    if not df[col].isnull().all():
        df[col] = df[col].str.strip()

    return df


def col_group(df, args):
    """
    To group the dataframe rows by columns
    """
    df = df.groupby(args).sum().reset_index()
    return df


def check_empty_column_add_value(df, args):
    """
    To add the column and its value in dataframe based on empty condition
    Example : column_to_add|condition_column|Column-values-separated-by-commas
    Example : metric_value|user_id|Total Visits,Visits
    """
    value = args[2].split(',')
    df[args[0]] = np.where(df[args[1]] == '', value[0], value[1])
    return df


def col_split_into_list(df, args):
    """
    To split the column into multiple columns by delimiter
    For ex : args = ['pushnotification'|'title,body,type,owner'|',']
    """
    col_initial = args[0]
    final_col_list = args[1]
    split_delimiter = args[2]
    final_col_list = final_col_list.split(split_delimiter)
 
    if col_initial in list(df.columns):
        df_new = pd.DataFrame(df[col_initial].apply(split_column_and_validate_length, final_col_length=len(final_col_list)).tolist(), columns=final_col_list)
        df = df.reset_index()
        df = pd.concat([df, df_new],axis=1)
    return df


def col_to_datetime(df, args):
    """ Convert column date string to datetime"""
    df[args[0]] = df[args[0]].apply(pd.to_datetime)
    return df


def col_validate_and_add(df_list, args):
    """ 
    To check the column and add the column in the dataframe if not present

    args[0]: The column to add
    args[1]: The value of column
    """

    for df_data in df_list:
        if args[0] not in list(df_data.columns):
            df_data = col_set(df=df_data, args=[args[0], args[1]])
    return df_list


def split_column_and_validate_length(name, final_col_length): 
    split_column_value = name.split('|')
    if len(split_column_value) == 4:
        if final_col_length == 3:
            return [split_column_value[0], split_column_value[3], split_column_value[1]]
        else:
            return split_column_value
    elif len(split_column_value) == 3:
        if final_col_length == 4:
            return [split_column_value[0],'' ,split_column_value[1], split_column_value[2]]
        return [split_column_value[0], split_column_value[1], split_column_value[2]]
    else:
        if final_col_length == 2:
            return [split_column_value[0], split_column_value[1]]
        elif final_col_length == 3:
            return [split_column_value[0], split_column_value[1], '']
        else:
            return [split_column_value[0], split_column_value[1], '', '']


def col_remove_row(df,args): 
    """To remove rows based on keywords
    For ex: col_remove_row=>content_type|Staying on track,Making you younger,Making you older|App

    Args:
        df ([DataFrame]): The source dataframe
        args ([list]): The parameter list
    where,
        args[0]: The column which has to be filtered
        args[1]: The keywords which need to be remove from the given column
        args[2]: The platform which is filtered

    Returns:
        [DataFrame]: The final output dataframe
    """
    
    col = args[0]
    remove_keyword = args[1]
    remove_keyword = remove_keyword.split(',')
    platform = args[2]
    if platform == 'Web': 
        df = df[~((df[col].isin(remove_keyword)) & (df['platform'] == platform))]
    else:
        df = df[~((df[col].isin(remove_keyword)) & (df['platform'] != platform))]
    
    return df



def col_filter_empty(df, args):
    """To remove empty, null, None, unauthenticated, unspecified rows
    For ex: col_filter_empty=>content_type

    Args:
        df ([DataFrame]): The source dataframe
        args ([list]): The parameter list
    where,
        args[0]: The column which has to be filtered

    Returns:
        [DataFrame]: The final output dataframe
    """
    column = args[0]

    unauthenticated = df[column] != "unauthenticated"
    unspecified = df[column] != "::unspecified::"
    invalid = df[column] != "Unspecified"
    unknown = df[column] != "unknown"
    empty = df[column] != ""
    zero = df[column] != 0
    not_null = df[column].notnull()
    df = df[unauthenticated & unspecified & invalid & unknown & zero & not_null & empty]
    return df


def col_initcase_title(df, args):
    """
    Converts values in column to capitalize the first letter of each word.
    """
    df[args[0]] = df[args[0]].str.title()
    return df


def col_split_content_name(df,args):
    col_initial = args[0]
    content_name_list=args[1].split(",")
    static_value_list=args[2].split(",")
    new_col =args[3]
    df_new = pd.DataFrame(df[col_initial].apply(split_and_validate_content_name,static_value_list=static_value_list,content_name_list=content_name_list).tolist(),columns=[new_col])
    df= pd.concat([df, df_new],axis=1)
    return df

def split_and_validate_content_name(value,static_value_list=[],content_name_list=[]):
    for video_name in content_name_list:
        return [static_value_list[1] if (value.lower()).__contains__(video_name.lower()) else static_value_list[0]]