from typing import Counter
import pandas as pd 
df1=pd.read_csv(f"scripts/pandas_files/csvfiles/etl_source.csv",sep="|")

df1=df1[df1['prop28']!="::unspecified::"]
df1=df1[df1['prop31']!="::unspecified::"]
df1=df1[df1['prop16']!="::unspecified::"]
df1=df1[df1['prop8']!="::unspecified::"]
print(df1)