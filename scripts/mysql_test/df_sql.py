from datetime import datetime
import mysql.connector as msc 
import pandas as pd
from pandas.core.dtypes import dtypes
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
    cols_1=df.columns
    cols_1=",".join([str(i) for i in cols_1.tolist()])
    
    for i,row in df.iterrows():
        #print(f"insert into test_db.{file_name} ({cols_1}) values{tuple(row)} " )
        sql=f"INSERT INTO test_db.{file_name}({cols_1}) VALUES{tuple(row)} "           
        mycursor.execute(sql)
        #break
    mydb.commit()

            
def  table_to_df(table_name):
    """Metod used to insert sql table into dataframe

    Args:
        table_name (str): name of a table

    Returns:
        object: dataframe of sql table
    """

    mydb=read_configconnection()
    db=read_config.getconfig("mysql","database")
    df=pd.read_sql(con=mydb, sql=f"SELECT * FROM {db}.{table_name}")
    return df



def create_table(file_name):
    """method used to create table on mysql server of dataframe in csv file 

    Args:
        file_name (str): name of csv file
    """

    df=pd.read_csv(f"scripts/pandas_test/csvfiles/{file_name}.csv",sep="|")
    
    mydb=read_configconnection()
    mycursor=mydb.cursor()
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
    #print(f"create table test_db.{file_name}({table_schema})")
    sql=f"CREATE TABLE {db}.{file_name}({table_schema})"
    mycursor.execute(sql)
    mydb.commit()

    



def main():
    file_name=input("Enter the csv file name")
    create_table(file_name)
    csv_to_table(file_name)


if __name__=="__main__":
    main()