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

def csv_to_table(df):
    mydb=read_configconnection()
    mycursor=mydb.cursor()
    cols=",".join([str(i) for i in df.columns.tolist()])
    
    for i,row in df.iterrows():
        sql=f"insert into test_db.new_class ({cols}) values {tuple(row)} "           
        mycursor.execute(sql)
    mydb.commit()
    
            
def  table_to_df():
    mydb=read_configconnection()
    df=pd.read_sql(con=mydb, sql="select * from test_db.data")
    return df



#def create_table(df):
dict={
       "Name":["abhinav","aakash","Ayansh","arpit","Rohan","Maynak"], 
       "Roll_no":[1,2,3,4,5,6],
       "Marks":[76,87,90,55,54,66],
       "Qualification":["B.Tech","BBA","BCA","BSC","B.Tech","BBA"]
       }
df=pd.DataFrame(dict)
cols=list(df.columns)
"""colm=list(df.columns)
for i in colm:
    print(type(df[i]))"""


#cols=",".join([str(i) for i in df.columns.tolist()])
#for i in cols:
   # sql="create table test_db.graduation_details(     )"
k=0
for i,j in df.iterrows():
    if k==0:
        tup=list(j)
        data_type=[]
        for item in tup:
            data_type.append(type(item))
    break

print(data_type)

table_schema=[]
j=0
for column_name in cols:
    
    table_schema.append(f"{column_name} {data_type[j]}")
    j=j+1




table_schema=",".join([str(i) for i in table_schema])
print(table_schema)
table_schema=[table_schema]
print(table_schema)