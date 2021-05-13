import pandas as pd 
import sys

def readcsv(l,set_list):
    n=int(input("enter the number of dataframe"))
    for i in range(0,n):
        path=input("enter path of file")
        df1=pd.read_csv(f"scripts/pandas_test/csvfile/{path}",sep="|")
        l.append(df1)
        set_list.append(set(df1.columns))
    return l


# function for merging a csv files
def merge(l,set_list):
    com_col=set()
    for i in range(0,len(set_list)):
        if i==0:
            com_col=com_col.union(set_list[i])
        else:
            com_col=com_col.intersection(set_list[i])
    list_1=list(com_col)
    df=pd.DataFrame()
    for i in range(0,len(l)):
        if i==0:
            df=pd.merge(l[0],l[1],how="outer",on=list_1).fillna(0)
        if i==1:
            continue
        else:
            df4=pd.merge(l[i],df,how="outer",on=list_1).fillna(0)
    return df4


#Function to filer 
def filer(df4):
    filter_value=input("enter the value which u want to use to filter row")
    for i in df4.columns:
        df4=df4[df4[i] !=filter_value]
    return df4


#function for melt dataframe
def meltdf(df4):
    df4=pd.melt(df4,id_vars=["datetime","datetime_friendly","prop28","prop31","prop16","prop8"],var_name="metric_name",value_name="metric_value")
    df4["metric_value"]=df4["metric_value"].astype(int)
    df4=df4[df4.metric_value>0]
    
    return df4


#function to save csv file
def savecsv(df4):
    file_name=input("Enter name want to save as .csv")
    df4.to_csv(file_name,sep="|")