import mmap
import pandas as pd
from lib import transform
def mmap_io(filename):
    with open(filename, mode="r", encoding="utf8") as f:
        etl_rules = [ line.strip() for line in f ]
        return etl_rules
    
def main():
    
    try:
        df=pd.read_csv(f"scripts/pandas_files/csvfiles/etl_source.csv",sep="|")
        
        file_name='scripts/pandas_files/csvfiles/etl_rule.map'
        etl_rules=mmap_io(file_name)
        for i in etl_rules:
            operation_args=i.split("=>")
            operation=operation_args[0]
            args=operation_args[1].split("|")
            df = getattr(transform, operation)(df,args)
        print(df)
    except Exception as e:
        print(e)
    #df.to_csv(f"scripts/pandas_files/csvfiles/etl_transformed.csv",sep="|",index=False)
if __name__=="__main__":
    main()
