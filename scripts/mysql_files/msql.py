from logging import exception
import mysql.connector as msc 
import pandas as pd
from library import read_config 

logger = read_config.logger()
pool_cnxn=read_config.mysl_pool_connection()
mycursor=pool_cnxn.cursor()


# Function to connect databse with python code


def create_table(table_name):

    database=read_config.get_config("mysql","database")

    cols=[]
    column=input("enter column name with thier data type")
    cols=column.split(",")
    cols= ",".join([str(i) for i in cols])

    try:
        sql=f"create table {database}.{table_name}({cols})"
        mycursor.execute(sql)
        logger.debug(f"create table {database}.{table_name}({cols}) ")
        pool_cnxn.commit()
    except Exception as e:
        logger.debug(f"exception arise :{e}")




# Function to display name of each database

def showallDatabases():
    """Method use to print all the database in a host"""

    
    mycursor.execute("show databases")
    for i in mycursor:
        print(i)


def fetchrecord(table_name):
    """Method is use to fetch the record from a specific table in a database"""

    database=read_config.get_config("mysql","database")
    choice=int(input('select choice by index \n 1:fetch all record \n 2:fetch all record for specific column\n 3:fetch record  of specific condition \n 4:fetch record as specific column for a specific condition '))
    try:
        if choice==1:
            
            sql=f"select * from {database}.{table_name}"
            mycursor.execute(sql)
            result=mycursor.fetchall()
            
            for record in result:
                print(record)
            logger.debug(f"data fetched from {table_name}")
           
        elif choice==2:
            l=input("Enter column names as comma seperated")
            sql=f"select {l} from {database}.{table_name}"
            mycursor.execute(sql)
            result=mycursor.fetchall()
            for record in result:
                print(result)
            logger.debug(f"data fetched from {table_name}")
        elif choice==3:
            cond=input("enter condition ")
            sql=f"select * from {database}.{table_name} where {cond}"
            mycursor.execute(sql)
            result=mycursor.fetchall()
            for record in result:
                print(record)
            logger.debug(f"data fetched from {table_name}")
        elif choice==4:
            l=input("Enter column names as comma seperated")
            cond=input("enter condition ")
            sql=f"select {l} from {database}.{table_name} where {cond} "
            mycursor.execute(sql)
            result=mycursor.fetchall()
            for record in result:
                print(record)
            logger.debug(f"data fetched from {table_name}")
    except Exception as error:
        print(f"Exception generated {error}")
        logger.error(f"Exception arrise : {error}")
    
        

def insertrecord(table_name):
    """ Method is used to insert record in a table"""
    
     
    database=read_config.get_config("mysql","database")

    cols=[]
    cols_name=input("Enter columns names")
    cols=cols_name.split(",")
    cols=",".join([str(i) for i in cols])
    list_1=[]
    list_element=input('Enter the column values')
    list_1=list_element.split(",")
    for i in range(0,len(list_1)):
        if list_1[i].isdigit():
            list_1[i]=int(list_1[i])
    col_val=tuple(list_1)

    try:
        mycursor.execute(f"insert into {database}.{table_name} ({cols}) values {col_val} ")
        pool_cnxn.commit()
        logger.debug(f"insert into {database}.{table_name} ({cols}) values {col_val} ")
    except Exception as error:
        print(f"Exception generated {error}")
        logger.error(f"Exception generated {error}")
    


def insertmanyrecord(table_name):
    """Method is used to insert more than one record at a time in a databsase table"""
    
    database=read_config.get_config("mysql","database")

    cols=[]
    cols_name=input("Enter columns names")
    cols=cols_name.split(",")
    para_len=len(cols)
    cols=",".join([str(i) for i in cols])
    no_of_record=int(input("Enter the number of record")) 
    l=[]
    val=[]
    for i in range(0,no_of_record):
        list_element=input('Enter the record')
        l=list_element.split(",")
        for i in range(0,len(l)):
            if l[i].isdigit():
                l[i]=int(l[i])
        val.append(tuple(l))
    parameters=["%s"]*para_len
    parameters=",".join([str(i) for i in parameters])
    try:
        sql=f"insert into {database}.{table_name}({cols}) values({parameters})"
        mycursor.executemany(sql,val)
        logger.debug(f"records {val} was successfully inserted in {table_name} ")
        pool_cnxn.commit()
    except Exception as error:
        print(f"Exception generated {error}")
        logger.debug(f"Exception generated {error}")
    

def updatecolvalue(table_name):
    """Method is used to update a column value in a table"""

    
    database=read_config.get_config("mysql","database")

    dict1=dict()
    cont="y"
    while cont=='y' or cont=='Y':
        colname=input("enter col_name whose values u want to updated")
        if colname.isdigit()==True:
            colname=int(colname)
        
        new_val=input("enter new value")
        
        if new_val.isdigit()==True:
            new_val=int(new_val)
        dict1.update({colname:new_val})
        cont=input("do you want to update more column y or n")
    
    cond=input("enter condition")
    try:
        for c_name,val in dict1.items():
            #print(f"update {database}.{table_name}  set {c_name} ={val}  where {cond}")
            sql=f"update {database}.{table_name}  set {c_name} ={val}  where {cond}" 
            mycursor.execute(sql)
            logger.debug(f"Successfuly upadate value of {c_name} to {val} where {cond} in {table_name}")
        pool_cnxn.commit()
    except Exception as error:
        logger.debug(f"Exception generated {error}")
        print(f"Exception generated {error}")
    


       

def deleterecord(table_name):
    """Method is used to delete record from database table
    """
    
    mycursor=pool_cnxn.cursor()
    database=read_config.get_config("mysql","database")

    cond=input("enter condition ")
    try:
        mycursor.execute(f"delete from {database}.{table_name} where {cond} ")
        pool_cnxn.commit()
        logger.debug(f"record was successfully deleted from {table_name} where {cond} ")
    except Exception as error:
        print(f"Exception generated {error}")
        logger.debug(f"Exception generated {error}")
    

           
def main():
   
    cont="y"
    while cont=='y' or cont=='Y':
        try:
            table_name=input("enter table_name")
            choice=int(input("Enter your choice \n 1: fetch record \n 2: insert record \n 3: insert many record \n 4: Delete records \n 5: update column values \n 6: create table"))
            if choice==1:
                fetchrecord(table_name)
            elif choice==2:
                insertrecord(table_name)
            elif choice==3:
                insertmanyrecord(table_name)
            elif choice==4:
                deleterecord(table_name)
            elif choice==5:
                updatecolvalue(table_name)
            elif choice==6:
                create_table(table_name)
        except ValueError as error:
            print(f"error arise : {error}")
            logger.error(f"error arise : {error}")
        except Exception as error:
            print(f"exception arise : {error}")
            logger.error(f"exception arise : {error}")

        cont=input("want to continue y or n")
    
    
    

if __name__=="__main__":
    main()

