import mysql.connector as msc 
from lib import read_config 

def read_configconnection():
    mydb=msc.connect(host=read_config.getconfig("mysql","host"),
                    user=read_config.getconfig("mysql","user"),
                    database=read_config.getconfig("mysql","database"),
                    password=read_config.getconfig("mysql","password"))
    return mydb

def showallDatabases():
    mydb=read_configconnection()
    mycursor=mydb.cursor()
    mycursor.execute("show databases")
    for i in mycursor:
        print(i)


def fetchRecoread_config():
    mydb=read_configconnection()
    mycursor=mydb.cursor()
    choice=int(input('select choice by index \n 1:fetch all recoread_config \n 2:fetch all recoread_config for specific column\n 3:fetch recoread_configs  of specific condition \n 4:fetch recoread_config as specific column for a specific condition '))
    try:
        if choice==1:
            try:
                mycursor.execute("select * from test_db.data")
                result=mycursor.fetchall()
                for recoread_config in result:
                    print(result)
            except:
                print("unknown error")
            finally:
                mydb.close()
        elif choice==2:
            l=input("Enter column names as comma seperated")
            mycursor.execute(f"select {l} from test_db.data")
            result=mycursor.fetchall()
            for recoread_config in result:
                print(result)
        elif choice==3:
            cond=input("enter condition ")
            mycursor.execute(f"select * from test_db.data where {cond}")
            result=mycursor.fetchall()
            for recoread_config in result:
                print(recoread_config)
        elif choice==4:
            l=input("Enter column names as comma seperated")
            cond=input("enter condition ")
            mycursor.execute(f"select {l} from test_db.data where {cond} ")
            result=mycursor.fetchall()
            for recoread_config in result:
                print(recoread_config)
    except Exception as error:
        print(f"Exception generated {error}")
    finally:
        mydb.close()
        

def insertrecoread_config():
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
        print("recoread_config was successfully inserted ")
        mydb.commit()
    except Exception as error:
        print(f"Exception generated {error}")
    finally:
        mydb.close()


def insertManyRecoread_configs():
    mydb=read_configconnection()
    mycursor=mydb.cursor()
    sql="insert into test_db.data (f_name,l_name,age,qualification,percentage) values(%s,%s,%s,%s,%s)"
    no_of_recoread_config=int(input("Enter the number of recoread_config")) 
    l=[]
    val=[]
    for i in range(0,no_of_recoread_config):
        list_element=input('Enter the recoread_config')
        l=list_element.split(",")
        for i in range(0,len(l)):
            if l[i].isdigit():
                l[i]=int(l[i])
        val.append(tuple(l))
    try:
        mycursor.executemany(sql,val)
        print("recoread_config was successfully inserted ")
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
        for recoread_config in result:
            print(recoread_config)
    except Exception as error:
        print(f"Exception generated {error}")
    finally:
        mydb.close()

def deleterecoread_config():
    mydb=read_configconnection()
    mycursor=mydb.cursor()
    cond=input("enter condition ")
    try:
        mycursor.execute(f"delete from test_db.data where {cond} ")
        print(f"recoread_config was successfully deleted from table where {cond} ")
        mydb.commit()
    except Exception as error:
        print(f"Exception generated {error}")
    finally:
        mydb.close()

def main():
    
    cont="y"
    while cont=='y' or cont=='Y':
        choice=int(input("Enter your choice \n 1: fetch recoread_config \n 2: insert recoread_config \n 3: insert many recoread_config \n 4: join \n 5: Delete recoread_configs \n 6: update column values"))
        if choice==1:
            fetchRecoread_config()
        elif choice==2:
            insertrecoread_config()
        elif choice==3:
            insertManyRecoread_configs()
        elif choice==4:
            join()
        elif choice==5:
            deleterecoread_config()
        elif choice==6:
            updatecolvalue()
        cont=input("want to continue y or n")

if __name__=="__main__":
    main()

