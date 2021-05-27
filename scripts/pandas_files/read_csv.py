import pandas as pd 
import argparse
parse=argparse.ArgumentParser()
def readcsvfile(file_name):
    try:
        df=pd.read_csv(f"scripts/pandas_files/csvfiles/{file_name}.csv",sep="|")
        print("file sucessfully saved")
        df.to_csv(f"scripts/pandas_files/csvfiles/task_2.csv",sep="|",index=False)
        return df 
    except FileNotFoundError as e:
        print(f"error : {e}")

def main():
    df=pd.DataFrame()
    result=readcsvfile("task_1")
    
    

if __name__=="__main__":
    main()