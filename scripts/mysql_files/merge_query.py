from lib import read_config

conn = read_config.mysl_pool_connection("mysql")
cursor = conn.cursor()

def get_new_query(table):
    sql="""SHOW KEYS FROM test_db.employee WHERE Key_name = 'PRIMARY'"""
    cursor.execute(sql)
    key=cursor.fetchone()
    cursor.execute("SHOW columns FROM employee")
    cols=[column[0] for column in cursor.fetchall()]
    cols.remove(key[4])
    col_str = ""
    for index,col in enumerate(cols):
        if index != 0:
            col_str= col_str+ ", "
        col_str += f"{col} = new.{col}"
    return col_str

def merge_query(table,values):
    parameters = ["%s"]*len(values[0])
    parameters=",".join([str(i) for i in parameters])
    sql = f""" INSERT INTO test_db.{table}  Values ({parameters})
        AS new ON DUPLICATE KEY UPDATE
        {get_new_query(table)}"""
    cursor.executemany(sql,values)
    conn.commit()
    
    
def show_table(table_name):
    sql = f"SELECT * FROM test_db.{table_name}"
    cursor.execute(sql)
    return cursor.fetchall()
    
def main():
    values=[(101,'Abhinav Kumar',22,'M','D-12'),(102,'Abhishek Chauhan',23,'M','D-21'),(107,'Arpit',25,'M','D-03'),(108,'Rishabh kasana',24,'M','D-19')]
    print(f"record before merge : {show_table('employee')}\n")
    merge_query("employee",values)
    print(f"record after merge : {show_table('employee')} ")
    
if __name__ == "__main__":
    main()