# importing pandas module
import pandas as pd 
 
# Define a dictionary containing employee data 
data1 = {'key': ['K0', 'K1', 'K2', 'K3'],
         'key1': ['K0', 'K1', 'K0', 'K1'],
         'Name':['Jai', 'Princi', 'Gaurav', 'Anuj'], 
        'Age':[27, 24, 22, 32],} 
   
# Define a dictionary containing employee data 
data2 = {'key': ['K0', 'K1', 'K2', 'K3'],
         'key1': ['K0', 'K0', 'K0', 'K0'],
         'Address':['Nagpur', 'Kanpur', 'Allahabad', 'Kannuaj'], 
        'Qualification':['Btech', 'B.A', 'Bcom', 'B.hons']} 
 
# Convert the dictionary into DataFrame  
df = pd.DataFrame(data1)
 
# Convert the dictionary into DataFrame  
df1 = pd.DataFrame(data2) 


"""single_key=pd.merge(df,df1,on='key')
print(single_key)"""

"""mul_key=pd.merge(df,df1,on=['key','key1'])
print(mul_key)"""


"""left=pd.merge(df,df1,how="left",on=['key','key1'])
print(left)"""
"""right=pd.merge(df,df1,how="right",on=['key','key1'])
print(right)"""