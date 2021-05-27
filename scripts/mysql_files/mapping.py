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


mydb=read_configconnection()
sql="show table"
mycursor=mydb.cursor()
mycursor.execute(sql)