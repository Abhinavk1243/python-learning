import pandas as pd
import numpy as np 
def makedataframe():
    continue_1='y'
    while continue_1=='y' or continue_1=='Y':
        col_name=input("enter the column name")
        if col_name.isdigit()==True:
            col_name=int(key)
        cols_data=input('Enter the columns data')
        list_1=cols_data.split(",")
        for i in range(0,len(list_1)):
            if list_1[i].isdigit():
                list_1[i]=int(list_1[i])
        data.update({col_name:list_1})
        continue_1=input("want to continue_1")
    df=pd.DataFrame(data)
    return df

data=dict()
cont='y'
while cont=='y' or cont=='Y':
    choice=int(input("enter choice \n 1: Make dataframe \n 2:sava as .csv file \n 3:read csv \n"))
    if choice==1:
        df=makedataframe()
        print(df)
    elif choice==2:
        file_name=input("enter the name of file in .csv format")
        df.to_csv(file_name)
    elif choice==3:
        file_name=input("entername of the  .csv file want to read")
        print(pd.read_csv(file_name))
    cont=input("want to continue")

