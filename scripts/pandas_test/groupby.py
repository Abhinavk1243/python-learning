import pandas as pd 
import numpy as np

data1 =  {'Name':['Jai', 'Anuj', 'Jai', 'Princi', 'Gaurav', 'Anuj', 'Princi', 'Abhi'],'Age':[27, 24, 22, 32, 33, 36, 27, 32],'Address':['Nagpur', 'Kanpur', 'Allahabad', 'Kannuaj','Jaunpur', 'Kanpur', 'Allahabad', 'Aligarh'],'Qualification':['Msc', 'MA', 'MCA', 'Phd','B.Tech', 'B.com', 'Msc', 'MA'],"Weight":[78,65,70,87,68,89,80,77]} 
df=pd.DataFrame(data1)

# group by address
gk=df.groupby("Name")
for i,j in gk:
    print(i)
    print(j)

#group by multiple keys(address and qualificatio )
gkm=df.groupby(["Name","Qualification"])
for i,j in gkm:
    print(i)
    print(j)

# get a single group
print(gkm.get_group(("Jai","Msc")))
print(gk.get_group("Jai"))

#apply statistic operation on numeric column
print(gk.aggregate([np.sum,np.mean,np.std]))
print(gk.agg({'Age':"sum","Weight":"std"}))



