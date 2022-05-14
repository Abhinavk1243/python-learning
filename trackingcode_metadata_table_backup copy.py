import gc
import logging
import argparse
import cursor
import numpy as np
import pandas as pd
import vertica_python
import mysql.connector
from lib import read_config
# from commons import Commons
from datetime import timedelta, datetime, date
# from commons_load_stats import commons_load_stats
import json
# Load stats initialization
# load_stats = commons_load_stats()



def get_new_query(schema,table,section):
    
    conn = read_config.mysl_pool_connection(section)
    cursor= conn.cursor()
    sql=f"SHOW KEYS FROM {schema}.{table} WHERE Key_name = 'PRIMARY'"
    print(sql)
    cursor.execute(sql)
    key=cursor.fetchone()
    
    cursor.execute(f"SHOW columns FROM {table}")
    cols=[column[0] for column in cursor.fetchall()]
    cols.remove(key[4])
    col_str = ""
    for index,col in enumerate(cols):
        if index != 0:
            col_str= col_str+ ", "
        col_str += f"{col} = new.{col}"
        
    conn.close()
    return col_str

def merge_query(schema,table,section,values):
    parameters = ["%s"]*len(values[0])
    parameters=",".join([str(i) for i in parameters])
    sql = f""" INSERT INTO {schema}.{table}  Values ({parameters})
        AS new ON DUPLICATE KEY UPDATE
        {get_new_query(schema,table,section)}"""
        
    print(sql)
    conn = read_config.mysl_pool_connection(section)
    cursor= conn.cursor()
    cursor.executemany(sql,values)
    conn.commit()
    conn.close
    
def get_json_config(configName):
    with open(f'{configName}.json') as config_file:
        config = json.load(config_file)
    return config

def read_data_from_db(schema, table, section):
    try:
        # logging.info("Creating connection with DB...")
        # db = Commons.db_config(section=section)
    
        if section == "dataops_mysql":
            conn = read_config.mysl_pool_connection("dataops_mysql")
            
            # connection = mysql.connector.connect(**db)
        else:
            # connection = vertica_python.connect(**db)
            conn = read_config.mysl_pool_connection("messaging")
        
        
        query = f"Select * from {schema}.{table}"
        tasks_df = pd.read_sql(sql=query, con=conn)
        return tasks_df
    except Exception as error:
        # logging.error(
            # f'Exception occurs in Adobe apple app download script : {error}')
        raise error
    finally:
        if conn is not None:
            conn.close()
            logging.info('Connection closed!!!')

def delete_duplicate_from_db(schema, table, section):
    try:
        logging.info("Creating connection with DB...")
        db = Commons.db_config(section=section)

        if section == "dataops_mysql":
            connection = mysql.connector.connect(**db)
        else:
            connection = vertica_python.connect(**db)

        delete_query = f"Delete from {schema}.{table}"
        cursor = connection.cursor()
        cursor.execute(delete_query)
        connection.commit()
        logging.info(f'Data delete from {schema}.{table}')
        
    except Exception as error:
        logging.error(
            f'Exception occurs in Adobe apple app download script : {error}')
        raise error
    finally:
        if connection is not None:
            connection.close()
            logging.info('Connection closed!!!')


def ingest_into_db(schema, table, melted_file, section):
    
    try:
        logging.info("Creating connection with DB...")
        db = Commons.db_config(section=section)

        if section =="dataops_mysql":
            connection = mysql.connector.connect(**db)
        else:
            connection = vertica_python.connect(**db)

        logging.info("Successfully create connection....")
        Commons.copy_to_vertica(
            connection=connection,
            schema=schema,
            target_table=table,
            file_delimiter="|",
            str_data=melted_file,
            abort=True,
        )
        logging.info(f'Data ingest into {schema}.{table}')

    except Exception as error:
        logging.error(
            f'Exception occurs in Adobe apple app download script : {error}')
        raise error
    finally:
        if connection is not None:
            connection.close()
            logging.info('Connection closed!!!')

def main(schema_df):
    logging.info("Stat taking backup for cmpid")
    schema = schema_df["schema"]
    table = schema_df["table"]
    df_cmpid_mysql = read_data_from_db("dataops_mysql", table,"dataops_mysql")
    df_cmpid_vertica = read_data_from_db(schema, table, "messaging")
    df_cmpid_vertica['last_updated_date']=df_cmpid_vertica['last_updated_date'].astype(str)

    # print(df_cmpid_vertica)
    values = list(df_cmpid_vertica.itertuples(index=False, name=None))
    # print(values)
    merge_query("dataops_mysql", table,"dataops_mysql",values)
    # bigdata = df_cmpid_vertica.append(df_cmpid_mysql, ignore_index=True)
    # bigdata = bigdata.drop_duplicates(subset='id', keep='last')

    # melted_file = bigdata.to_csv(sep="|", encoding="utf-8", header=None, index=False)
    # delete_duplicate_from_db("SC_OMNITURE", "sc3_cmpid", "vertica_adobe")
    # ingest_into_db("SC_OMNITURE", "sc3_cmpid", melted_file, "vertica_adobe")   
    # load_stats.target_count =  load_stats.target_count + len(bigdata)
    # load_stats.source_count = load_stats.source_count + len(df_cmpid_mysql)
    # logging.info(f'cmpid count {len(bigdata)}')
    # logging.info('Backup completed for cmpid')   
    
    # logging.info("Stat taking backup for cmpid meta data")
    # df_metadata_mysql = read_data_from_db("dataops_dashboard", "custio_sc_cmpid_metadata", "dataops_mysql")
    # df_metadata_vertica = read_data_from_db("SC_OMNITURE", "sc3_cmpid_metadata", "vertica_adobe")

    # bigdata = df_metadata_vertica.append(df_metadata_mysql, ignore_index=True)
    # bigdata = bigdata.drop_duplicates(['value', 'type'], keep='last')
    # melted_file = bigdata.to_csv(sep="|", encoding="utf-8", header=None, index=False)

    # delete_duplicate_from_db("SC_OMNITURE", "sc3_cmpid_metadata", "vertica_adobe")
    # ingest_into_db("SC_OMNITURE", "sc3_cmpid_metadata", melted_file, "vertica_adobe")
    # # load_stats.target_count =  load_stats.target_count + len(bigdata)
    # # load_stats.source_count = load_stats.source_count + len(df_metadata_mysql)
    # logging.info(f'cmpid metadata count {len(bigdata)}')
    # logging.info('Backup completed for cmpid meta data.')   


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='CustomerIO API Ingest Process',
                                    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                    allow_abbrev=False)

    parser.add_argument('--area', '-a',
                        type=str,
                        dest="area",
                        required=True,
                        help='CustomerIO area to process')
    parser.add_argument('--site', '-w',
                        type=str,
                        dest="site",
                        required=True,
                        help='CustomerIO worksite to process')
    
    args, unknown = parser.parse_known_args()
    area = args.area
    area = str(area).lower()

    site = args.site
    schema_config = get_json_config(configName='customerio_api_schema_config')
    
    schema_def = schema_config[site]
    schema_def["table"] = schema_def["table"] +area
    print(schema_def)

   
    
    try:
         # Job Stats
        job_type = f"Tracking Code Metadata Table ETL Script"
        status = "running"
        source_system_name = "MySql"
        target_system_name = "Vertica"
        source_system_location = "dataops_dashboard"
        target_system_location = "SC_OMNITURE"
        # logging.info(f'**************Executing : {job_type}********************')
        
        # Insert into job stats table only if entry not created previously
        # if not load_stats.job_id:
        #     load_stats.insert_job_start_log(job_type, status, source_system_name, target_system_name, source_system_location, target_system_location)
        #     load_stats.target_count = 0
        #     load_stats.source_count = 0


        main(schema_def)
        # logging.info(f'Source Count = {load_stats.source_count} and Target Count = {load_stats.target_count}')
        # load_stats.update_job_complete_log()

    except Exception as ex:
        # logging.error(f"error: {ex}" , exc_info=True)
        # load_stats.update_job_failed_log(ex)
        raise ex
    finally:
        ## Garbage collection
        collected = gc.collect()
        # logging.info(f"Garbage collector : collected {collected} objects.")


# area_def = config[area]

#         ## Table to process area for site
#         worksite_schema_def = schema_config[site]
#         area_def['schema'] = worksite_schema_def['schema']
#         area_def['table'] = worksite_schema_def['table'] + area