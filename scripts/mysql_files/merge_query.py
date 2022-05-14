from lib import read_config

conn = read_config.mysl_pool_connection("mysql")
cursor = conn.cursor()

def get_new_query(table):
    sql="""SHOW KEYS FROM test_db.employee WHERE Key_name = 'PRIMARY'"""
    cursor.execute(sql)
    key=cursor.fetchone()
    print(key)
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
     # {get_new_query(table)}
    parameters=",".join([str(i) for i in parameters])
    sql = f""" INSERT INTO test_db.{table}  Values ({parameters})
        AS new ON DUPLICATE KEY UPDATE
        counts = new.counts
        
        """
        
    # print(sql)
    cursor.executemany(sql,values)
    conn.commit()
    
    
def show_table(table_name):
    sql = f"SELECT * FROM test_db.{table_name}"
    cursor.execute(sql)
    return cursor.fetchall()
    
def main():
    values=[('[Consumer] Onboarding (3 Series)' ,'sent','2022-02-22',82),
  ('[Consumer] Onboarding (3 Series)' ,'delivered','2022-02-22',82),
   ('[Consumer] Onboarding (3 Series)' ,'opened','2022-02-22',55),
     ('[ENT] RAT Results WIP','delivered','2022-02-22',72),
     ('[ENT] RAT Results WIP','clicked','2022-02-22',45),
      ('[ENT] RAT Results WIP' ,'sent','2022-02-22',82),
        ('[sponsor_hp_sccarefirst] CareFirst Daily Scale Back Campaign','delivered','2022-02-22',96),
     ('[sponsor_hp_sccarefirst] CareFirst Daily Scale Back Campaign','clicked','2022-02-22',35),
      ('[sponsor_hp_sccarefirst] CareFirst Daily Scale Back Campaign' ,'sent','2022-02-22',92)]
    # print(f"record before merge : {show_table('employee')}\n")
    merge_query("main1",values)
    # print(f"record after merge : {show_table('employee')} ")
    
if __name__ == "__main__":
    main()