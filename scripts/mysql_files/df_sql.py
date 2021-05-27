from datetime import datetime
import mysql.connector as msc 
import pandas as pd
import logging as lg 
logger = lg.getLogger(__name__)
logger.setLevel(lg.DEBUG)
formatter = lg.Formatter('%(asctime)s : %(name)s :%(levelname)s : %(funcName)s :%(lineno)d : %(message)s ')


file_handler =lg.FileHandler("scripts/loggers_test/df_sql.log")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
from lib import read_config 

# Function to connect databse with python code
def read_configconnection():
    """Metod is use to connect database with python 

    Returns:
        connection : myslconnection
    """
    mydb=msc.connect(host=read_config.getconfig("mysql","host"),
                    user=read_config.getconfig("mysql","user"),
                    database=read_config.getconfig("mysql","database"),
                    password=read_config.getconfig("mysql","password"))
    return mydb

def csv_to_table(file_name):
    """ Method insert a data of csv file in sql table

    Args:
        file_name (str): Name of .csv file
    """

    df=pd.read_csv(f"scripts/pandas_test/csvfiles/{file_name}.csv",sep="|")
    mydb=read_configconnection()
    mycursor=mydb.cursor()
    database=read_config.getconfig("mysql","database")
    
    cols_1=df.columns
    cols_1=",".join([str(i) for i in cols_1.tolist()])
    try:
        for i,row in df.iterrows():
            #print(f"insert into test_db.{file_name} ({cols_1}) values{tuple(row)} " )
            sql=f"INSERT INTO {database}.{file_name}({cols_1}) VALUES{tuple(row)} "           
            mycursor.execute(sql)
            #break
        logger.debug(f"csv file : {file_name} is successfully inserted in database table : {file_name} ")
    except Exception as error:
        logger.error(f"Exception arise : {error}")
    
    finally:
        mydb.commit()

            
def  table_to_csv(table_name,file_name):
    """Metod used to insert sql table into dataframe

    Args:
        table_name (str): name of a table
        file_name (str): name csv file in which the sql table is need to stored

    Returns:
        object: dataframe of sql table
    """

    mydb=read_configconnection()
    db=read_config.getconfig("mysql","database")
    try:
        df=pd.read_sql(con=mydb, sql=f"SELECT * FROM {db}.{table_name}")
        df.to_csv(f"scripts/pandas_test/csvfiles/{file_name}.csv",sep="|",index=False)
        logger.debug(f"data of table : {table_name}  is stored in csv file :{file_name} ")  
    except Exception as error:
        logger.error(f"Exception arise : {error}")
    finally:
        mydb.close()

        

   
def create_table(file_name,table_name):
    """method used to create table on mysql server of dataframe in csv file 

    Args:
        file_name (str): name of csv file
        table_name (str): name of table want to created
    """
    mydb=read_configconnection()
    mycursor=mydb.cursor()

    try:
        df=pd.read_csv(f"scripts/pandas_test/csvfiles/{file_name}.csv",sep="|")
    except FileExistsError as error:
        logger.error(f"error arise : {error}")
    except Exception as error:
        logger.error(f"Exception arise : {error}")
    
    cols=list(df.columns)

    k=0
    for i,j in df.iterrows():
        if k==0:
            tup=list(j)
            data_type=[]
            for item in tup:
                data_type.append(item)
        break


    table_schema=[]
    k=0
    first=0
    for col in cols:
        if isinstance(data_type[k],int):
            table_schema.append(f"{col} int")
        elif isinstance(data_type[k],str):
            table_schema.append(f"{col} TEXT")
        elif isinstance(data_type[k],float):
            table_schema.append(f"{col} decimal(6)")
        elif isinstance(data_type[k],datetime):
            table_schema.append(f"{col} datetime(fsp)")
        first=1
        k=k+1

    table_schema=",".join([str(i) for i in table_schema])
    db=read_config.getconfig("mysql","database")

    try:
        #print(f"create table test_db.{file_name}({table_schema})")
        sql=f"CREATE TABLE {db}.{file_name}({table_schema})"
        mycursor.execute(sql)
        mydb.commit()
        logger.debug(f"create table {db}.{table_name}({cols}) ")
    except Exception as error:
        logger.error(f"exception arise : {error}")

    



def main():
    table_to_csv("students","students")


if __name__=="__main__":
    main()