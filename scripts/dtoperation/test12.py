from codecs import encode
import mysql.connector as msc 
import pandas as pd
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

"""cols=[]
column=input("enter column name with thier data type")
cols=column.split(",")
print(cols)
c=cols
c1=cols"""
"""table_schema=[]
k=0
first=0
for col in cols:
    ta"""

"""cols=[]
cols_name=input("Enter columns names")
cols=cols_name.split(",")
para_len=len(cols)
cols=",".join([str(i) for i in cols])"""
  
    

"""c= ",".join([str(i) for i in c])
c1= ",".join([str(i) for i in c1])
print(c)
print(c1)"""

x,y,z=[int(a) for a in input("enter x,y,z ").split(',')]
print(type(x))
print(y)
print(z)