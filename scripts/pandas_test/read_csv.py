import pandas as pd 
import argparse
parse=argparse.ArgumentParser()
def readcsvfile(args):
    try:
        df=pd.read_csv(f"scripts/pandas_test/csvfiles/{args.path}",sep="|")
        print("file sucessfully saved")
        print(df)
    except FileNotFoundError as e:
        print(f"error : {e}")

def main():
    parse.add_argument("path",type=str)
    arg=parse.parse_args()
    readcsvfile(arg)
    
if __name__=="__main__":
    main()