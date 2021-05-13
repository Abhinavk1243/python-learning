import pandas as pd 
import numpy as np
data1 = {'Name':['Jai', 'Princi', 'Gaurav', 'Abhi','Abhinav', 'Ayushi', 'Dhiraj', 'Hitesh'],  'Age':[27, 24,32, 14, 12, 52, 22, 32],  'Address':['Nagpur', 'Kanpur', 'Allahabad', 'Kannuaj','Kannuaj', 'Kanpur', 'Allahabad', 'Kannuaj'], 'Qualification':['Msc', 'MA', 'MCA', 'Phd','Phd', 'B.A', 'Bcom', 'B.hons']} 
df=pd.DataFrame(data1)
#g=df.groupby(["Address"])
#for i,j in g:
    #print(i)
    #print(j)
#print(g.get_group('Kannuaj'))
#agg1=g["Age"].agg([np.sum,np.mean,np.std])
#print(agg1)
#sc=lambda x:(x-x.mean())/x.std()*10
#print(g.transform(sc))
#g=df['Name'].groupby(df["Address"])
#for i,j in g:
 #   print(i)
  #  print(j)
df["Name"]=df["Name"].str.lower() # to lower case 
print(df)
#df["Age"]=df["Age"].replace(52,32)# replace data
# print(df)
#new=df["Address"].copy()
#df["Name"]=df["Name"].str.cat(new,sep=", ")
#print(df)