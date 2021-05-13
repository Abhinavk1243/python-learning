import pandas as pd 
file_name=input("Enter file name")
df=pd.read_csv(f"scripts/pandas_test/csvfile/{file_name}")
print(df)
