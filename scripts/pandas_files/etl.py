import mmap
import pandas as pd
from lib import transform


def mmap_io(filename):
    with open(filename, mode="r", encoding="utf8") as f:
        etl_rules = [ line.strip() for line in f ]
        return etl_rules
    
def col_rename(a={},b=None,c=None):
    print(a)
    print(b)
    print(c)



data={'id':[4,1,2],
    'name':['abhinav','abhishek','aakash'],
    'age':[23,21,20]
}

df=pd.DataFrame(data)

file_name='scripts/pandas_files/csvfiles/etlrul.map'
etl_rules=mmap_io(file_name)
for i in etl_rules:
    function_args=i.split("=>")
    function_name=function_args[0]
    args=function_args[1].split("|")
    args.insert(0,df)
    params=tuple(args)
    print(args)
    getattr(operation,function_name)(*params)
    operation(*params)
    break
print(df)
"""function_name='mmap_io'
result = eval(function_name + "(file_)")"""
