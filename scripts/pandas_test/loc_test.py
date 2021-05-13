import pandas as pd 
df1=pd.DataFrame({"Name":["aakash","abhishek"],"roll_no":["::unspecified",3],"maths":[45,39]})
df2=pd.DataFrame({"Name":["abhi","aakash","abhishek"],"roll_no":[1,"::unspecified",3],"Physic":[45,39,32]})
df3=pd.DataFrame({"Name":["::unspecified","aakash","abhishek"],"roll_no":[1,"::unspecified",3],"chemistry":[33,35,40]})
df=pd.merge(df1,df2,how="outer",on=["Name","roll_no"]).fillna(0)
df=pd.merge(df,df3,how="outer",on=["Name","roll_no"]).fillna(0)
print(df)
l=df.index
l1=["Name","roll_no"]
for i in l:
    for j in l1:
        if df.loc[i,j]=="::unspecified":
            df.drop(i, inplace = True,axis=0)
            break
print(df)