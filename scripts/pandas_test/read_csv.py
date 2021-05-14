import pandas as pd 
df=pd.read_csv(f"scripts/pandas_test/csvfiles/marks.csv")
df.to_csv("scripts/pandas_test/csvfiles/marks.csv",sep="|")

