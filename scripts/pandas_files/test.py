from typing import Counter
import pandas as pd 
df1=pd.read_csv(f"scripts/pandas_files/csvfiles/push_notification_raw_0.csv",sep="|")
df2=pd.read_csv(f"scripts/pandas_files/csvfiles/push_notification_raw_1.csv",sep="|")
df3=pd.read_csv(f"scripts/pandas_files/csvfiles/push_notification_raw_2.csv",sep="|")
df4=pd.read_csv(f"scripts/pandas_files/csvfiles/push_notification_raw_4.csv",sep="|")
list_1=["datetime","datetime_friendly","prop28","prop31","prop16","prop8"]
l=[df1,df2,df3,df4]
df=pd.DataFrame()
"""for i in range(0,len(l)):
    if i==0:
        df=pd.merge(l[0],l[1],how="outer",on=list_1).fillna(0)
        print(df)
    if i==1:
        continue
    else:
        df=pd.merge(l[i],df,how="outer",on=list_1).fillna(0)
    """
counter=0
for i in l:
    if counter==0:
        df=i
        counter=counter+1
    else:
        df=pd.merge(i,df,how="outer",on=list_1).fillna(0)


print(df)