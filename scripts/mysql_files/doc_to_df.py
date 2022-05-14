import os
import gc
from lib.read_config import logger
import numpy as np
import pandas as pd
# from pandas.io.json import json_normalize
import re

logging = logger()
def main():
    print("started......")
    

    data = [
        {
            'program_id': 'prog-1', 
            'eligibility': {
                'conditions': ['cond-1-1', 'cond-1-2'], 
                'tags': ['tag-1-3', 'tag-1-4'], 
                'events':[
                    {'eventType':'event-type-1', 'description': 'event-desc-1', 'eventIdentifier': 'event-identf-1'},
                    {'eventType':'event-type-2', 'description': 'event-desc-2', 'eventIdentifier': 'event-identf-2'}
                ]
            }
        },
        {
            'program_id': 'prog-2', 
            'eligibility': {
                'conditions': ['cond-2-5', 'cond-2-6'], 
                'tags': ['tag-2-7', 'tag-2-8'],
                'events':[
                    {'eventType':'event-type-3', 'description': 'event-desc-3', 'eventIdentifier': 'event-identf-3'},
                    {'eventType':'event-type-4', 'description': 'event-desc-4', 'eventIdentifier': 'event-identf-4'}
                ]
            }
        }
    ]
    df = pd.json_normalize(data)
    
    
    # print(df)
    

    df = col_rename(df, ['eligibility.conditions','eligibility_conditions'])
    df = col_rename(df, ['eligibility.tags','eligibility_tags'])
    df = col_rename(df, ['eligibility.events','eligibility_events'])
    
    # print(df)
    # "program_id|event_group_id|event_id|eligibility_type|eligibility_value|eligibility_description|eligibility_name|deleted_flg|deleted_dt\n";

    print('-----------------exploding------------')
    df = explode_column(df, ['eligibility_conditions'])
    # print(df)
    df = col_append_string(df, ['eligibility_conditions', 'condition', '==>'])
    # print(df)
    df['eligibility_conditions'] = df.apply(lambda x: '{}==>{}'.format(x.eligibility_conditions, ''), axis=1)
    df['eligibility_conditions'] = df.apply(lambda x: '{}==>{}'.format(x.eligibility_conditions, ''), axis=1)
    df = explode_column(df, ['eligibility_tags'])
    df = col_append_string(df, ['eligibility_tags', 'tag', '==>'])
    df['eligibility_tags'] = df.apply(lambda x: '{}==>{}'.format(x.eligibility_tags, ''), axis=1)
    df['eligibility_tags'] = df.apply(lambda x: '{}==>{}'.format(x.eligibility_tags, ''), axis=1)

    df = explode_column(df, ['eligibility_events'])
    
    df = flatten_column(df, ['eligibility_events','eventType:eligibility_event_value','description:eligibility_event_description','eventIdentifier:eligibility_event_name'])
    
    df = col_drop(df, ['eligibility_events'])
    df = col_rename(df, ['eligibility_event_value', 'eligibility_events'])

    df = col_append_string(df, ['eligibility_events', 'event', '==>'])
    df = col_combine(df, args=['eligibility_events', 'eligibility_event_description', '==>'])
    df = col_combine(df, args=['eligibility_events', 'eligibility_event_name', '==>'])
    df = col_drop(df, ['eligibility_event_description'])
    df = col_drop(df, ['eligibility_event_name'])
    # print(df)

    # print('---------------')
    # print(list(df.columns))
    # print('---------------')


    df = col_melt_from_list(df, args=['eligibility_conditions,eligibility_tags,eligibility_events', 'eligibility_type', 'eligibility_value'])
    # print(df)

    # print('------------------------')
    

    df = col_split_by(df, ['eligibility_value','eligibility_value,eligibility_type,eligibility_description,eligibility_name','==>'])
    # print(df)
    df = df.drop_duplicates()
    print('-------------------FINAL--------------------')
    # print(df)


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
        logging.debug(f"converting column:{args[0]} datatype to object")
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


if __name__ == "__main__":
    try:
        
        # main()
        # target_collections_list = {'eventType':'event-type-1', 'description': 'event-desc-1', 'eventIdentifier': 'event-identf-1'}
        # count_dict = dict.fromkeys(target_collections_list,0)
        # print(count_dict)
        
        # dict_1 = {"a":1,"b":2}
        # print(dict_1.get("a",4))
        # logging.debug('Successfully completed.')
        
        from jsonschema import Draft4Validator

        schema = {
            "$schema": "http://json-schema.org/schema#",
            "type": "array",
            "items": {
                "type": "object",
                
            "properties": {
                "name": {"type": "string"},
                "email": {"type": "string"},
                "gender":{"type":"string"}
            },
            "required": ["email"]}
        }
        
        json = [{"name":2,"email":1,"gender": 1},{"name":12,"email":"1","gender":"male"}]
        
        validator = Draft4Validator(schema = schema)
        errors = validator.iter_errors(instance=json)
        # Draft4Validator.check_schema(schema)
        for error in errors:
            print(f"column:{list(error.path)}, error:{error.message}")
            print(error.message.split("is not"))
            if (len(list(error.path))) >2:
                print("true")

    except Exception as error:
        logging.error(f'Exception occurs : {error}')
