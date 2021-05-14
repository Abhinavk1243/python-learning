import mysql.connector as msc 
from lib import read_config 

# Function to connect databse with python code
def read_configconnection():
    mydb=msc.connect(host=read_config.getconfig("mysql","host"),
                    user=read_config.getconfig("mysql","user"),
                    database=read_config.getconfig("mysql","database"),
                    password=read_config.getconfig("mysql","password"))
    return mydb

# Function to display name of each database

def showallDatabases():
    mydb=read_configconnection()
    mycursor=mydb.cursor()
    mycursor.execute("show databases")
    for i in mycursor:
        print(i)


def fetchrecord():
    mydb=read_configconnection()
    mycursor=mydb.cursor()
    choice=int(input('select choice by index \n 1:fetch all record \n 2:fetch all record for specific column\n 3:fetch record  of specific condition \n 4:fetch record as specific column for a specific condition '))
    try:
        if choice==1:
            try:
                mycursor.execute("select * from test_db.data")
                result=mycursor.fetchall()
                for record in result:
                    print(result)
            except:
                print("unknown error")
            finally:
                mydb.close()
        elif choice==2:
            l=input("Enter column names as comma seperated")
            mycursor.execute(f"select {l} from test_db.data")
            result=mycursor.fetchall()
            for record in result:
                print(result)
        elif choice==3:
            cond=input("enter condition ")
            mycursor.execute(f"select * from test_db.data where {cond}")
            result=mycursor.fetchall()
            for record in result:
                print(record)
        elif choice==4:
            l=input("Enter column names as comma seperated")
            cond=input("enter condition ")
            mycursor.execute(f"select {l} from test_db.data where {cond} ")
            result=mycursor.fetchall()
            for record in result:
                print(record)
    except Exception as error:
        print(f"Exception generated {error}")
    finally:
        mydb.close()
        

def insertrecord():
    mydb=read_configconnection()
    mycursor=mydb.cursor()
    list_1=[]
    list_element=input('Enter the column values')
    list_1=list_element.split(",")
    for i in range(0,len(list_1)):
        if list_1[i].isdigit():
            list_1[i]=int(list_1[i])
    col_val=tuple(list_1)
    try:
        mycursor.execute("insert into test_db.data (f_name,l_name,age,qualification,percentage) values (%s,%s,%s,%s,%s) ",col_val)
        print("record was successfully inserted ")
        mydb.commit()
    except Exception as error:
        print(f"Exception generated {error}")
    finally:
        mydb.close()


def insertmanyrecord():
    mydb=read_configconnection()
    mycursor=mydb.cursor()
    sql="insert into test_db.data (f_name,l_name,age,qualification,percentage) values(%s,%s,%s,%s,%s)"
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
    try:
        mycursor.executemany(sql,val)
        print("record was successfully inserted ")
        mydb.commit()
    except Exception as error:
        print(f"Exception generated {error}")
    finally:
        mydb.close()

def updatecolvalue():
    mydb=read_configconnection()
    mycursor=mydb.cursor()
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
            sql=f"update test_db.data set  {c_name}  ='{val}'  where {cond}" 
            mycursor.execute(sql)
            print(f"Successfuly upadate {c_name} at {val} where {cond}")
        mydb.commit()
    except Exception as error:
        print(f"Exception generated {error}")
    finally:
        mydb.close()

def join():
    mydb=read_configconnection()
    mycursor=mydb.cursor()
    inner="select * from test_db.student inner join test_db.student_course on test_db.student.roll_no=test_db.student_course.roll_no "
    left="select * from test_db.student left join test_db.student_course on test_db.student.roll_no=test_db.student_course.roll_no "
    right ="select * from test_db.student right join test_db.student_course on test_db.student.roll_no=test_db.student_course.roll_no "
    choice=int(input("enter your choice for join \n 1:Right join \n 2: left join \n 3: inner join"))
    try:
        if choice==1:
            mycursor.execute(right)
        elif choice==2:
            mycursor.execute(left)
        elif choice==3:
            mycursor.execute(inner)
        result=mycursor.fetchall()
        for record in result:
            print(record)
    except Exception as error:
        print(f"Exception generated {error}")
    finally:
        mydb.close()

def deleterecord():
    mydb=read_configconnection()
    mycursor=mydb.cursor()
    cond=input("enter condition ")
    try:
        mycursor.execute(f"delete from test_db.data where {cond} ")
        print(f"record was successfully deleted from table where {cond} ")
        mydb.commit()
    except Exception as error:
        print(f"Exception generated {error}")
    finally:
        mydb.close()

def main():
    
    cont="y"
    while cont=='y' or cont=='Y':
        choice=int(input("Enter your choice \n 1: fetch record \n 2: insert record \n 3: insert many record \n 4: join \n 5: Delete records \n 6: update column values"))
        if choice==1:
            fetchrecord()
        elif choice==2:
            insertrecord()
        elif choice==3:
            insertmanyrecord()
        elif choice==4:
            join()
        elif choice==5:
            deleterecord()
        elif choice==6:
            updatecolvalue()
        cont=input("want to continue y or n")

if __name__=="__main__":
    main()

