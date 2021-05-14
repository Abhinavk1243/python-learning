import pandas as pd 
try:
    df=pd.read_csv(f"scripts/pandas_test/csvfiles/marks.csv")
    df.to_csv("scripts/pandas_test/csvfiles/marks.csv",sep="|")
    print("file sucessfully saved")
except FileNotFoundError as e:
    print(f"error : {e}")
