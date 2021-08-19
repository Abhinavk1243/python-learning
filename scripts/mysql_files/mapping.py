import mysql.connector as msc 
import pandas as pd
from library import read_config 

logger = read_config.logger()
pool_cnxn=read_config.mysl_pool_connection()
mycursor=pool_cnxn.cursor()

# INITIALIZE EMPTY LIST
list_1=[]

def validation(teacher_id,class_id,course_id):
    database=read_config.get_config("mysql","database")
    mycursor.execute(f"select * from {database}.class_course;")
    class_course=mycursor.fetchall()
    mycursor.execute(f"select * from {database}.teacher_course;")
    teacher_course=mycursor.fetchall()
    tup_teacher_course=(teacher_id,course_id)
    tup_class_course=(class_id,course_id)
    cond_1=tup_teacher_course in teacher_course 
    cond_2=tup_class_course in class_course
    cond_3=(class_id,course_id) not in list_1

    if cond_1 and cond_2 and cond_3:
        list_1.append((class_id,course_id))
        tup_teacher_course=tuple()
        tup_class_course=tuple()
        return True
    else:
        return False

def insert_teacher_Class():
    database=read_config.get_config("mysql","database")
    no_of_record=int(input("Enter the number of record")) 
    l=[]
    val=[]
    for i in range(0,no_of_record):
        try:
            teacher_id,class_id,course_id=[int(a) for a in input("Enter teacher_id , class_id and course_id").split(',')]
        except ValueError as error:
            print(f"Error arise : {error}")
            logger.debug(f"Error arise : {error}")
        isvalid=validation(teacher_id,class_id,course_id)
        
        if isvalid==True:
            tuple_1=(teacher_id,class_id)
            val.append(tuple_1)
        else:
            print(f"({teacher_id,class_id}) is wrong entry, please insert correct entry")
            logger.error(f"({teacher_id,class_id}) is wrong entry")
    try:
        sql=f"insert into {database}.teacher_class(teacher,class) values(%s,%s)"
        mycursor.executemany(sql,val)
        print(f"records {val} was successfully inserted in teacher_class ")
        logger.debug(f"records {val} was successfully inserted in teacher_class ")
        pool_cnxn.commit()
    except Exception as error:
        print(f"Exception generated {error}")
        logger.debug(f"Exception generated {error}")
    
def main():
    insert_teacher_Class()

if __name__=="__main__":
    main()

    