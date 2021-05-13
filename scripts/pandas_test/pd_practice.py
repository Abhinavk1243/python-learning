# concat string to series 
import pandas as pd 
data1 = {'Name':['Jai', 'Princi', 'Gaurav', 'Anuj'], 
        'Age':[27, 24, 22, 32], 
        'Address':['Nagpur', 'Kanpur', 'Allahabad', 'Kannuaj'], 
        'Qualification':['Msc', 'MA', 'MCA', 'Phd']} 
df=pd.DataFrame(data1)
ser=df["Address"].copy()
df["Name"]=df["Name"].str.cat(ser,sep=", ")
df=df.rename(columns={"Name":"Name, Address"})
print(df)
print(df.drop("Address",axis=1))




