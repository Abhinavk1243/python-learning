#Merging
import pandas as pd 
 
# Define a dictionary containing employee data 
data1 = {'Name':['Jai', 'Princi', 'Gaurav', 'Anuj'], 
        'Age':[27, 24, 22, 32], 
        'Address':['Nagpur', 'Kanpur', 'Allahabad', 'Kannuaj'], 
        'Qualification':['Msc', 'MA', 'MCA', 'Phd'],
        'Mobile No': [97, 91, 58, 76]} 
   
# Define a dictionary containing employee data 
data2 = {'Name':['Gaurav', 'Anuj', 'Dhiraj', 'Hitesh'], 
        'Age':[22, 32, 12, 52], 
        'Address':['Allahabad', 'Kannuaj', 'Allahabad', 'Kannuaj'], 
        'Qualification':['MCA', 'Phd', 'Bcom', 'B.hons'],
        'Salary':[1000, 2000, 3000, 4000]} 
s=pd.Series([10000,20000,25000,15000],name="salary")
# Convert the dictionary into DataFrame  
df = pd.DataFrame(data1,index=[0, 1, 2, 3])
 
# Convert the dictionary into DataFrame  
df1 = pd.DataFrame(data2, index=[2, 3, 6, 7]) 
 
#print(df, "\n\n", df1) 
l=[df,df1]
# merge using concat
"""
merge=pd.concat(l)
print(merge)"""

#merge using set logic on axes
merge_1=pd.concat(l,axis=1,join="inner")
#merge_2=pd.concat(l,axis=1,join=outer)
#merge_3=pd.concat(l,axis=1,join=left)
#merge_4=pd.concat(l,axis=1,join=right)
print(merge_1)
#print(merge_2)
#print(merge_3)
#print(merge_4)
#merge df with series
"""merge_2=pd.concat([df,s],axis=1)
print(merge_2)"""
