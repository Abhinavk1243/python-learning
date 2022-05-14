import pandas as pd 
data1 = {'Name':['Jai', 'Princi', 'Gaurav', 'Anuj'], 
        'Age':[27, 24, 22, 32]} 
    
# Define a dictionary containing employee data 
data2 = {'Address':['Allahabad', 'Kannuaj', 'Allahabad', 'Kannuaj'], 
        'Qualification':['MCA', 'Phd', 'Bcom', 'B.hons']} 
  
# Convert the dictionary into DataFrame  
df = pd.DataFrame(data1)
dict_1={}
# Convert the dictionary into DataFrame  
df1 = pd.DataFrame(data2)
#print(df ,'\n\n', df1)

#outer = df.join(df1,how='outer')
#print(outer)
#inner = df.join(df1,how='inner')


#left = df.join(df1,how='left')
#right = df.join(df1,how='right')
"""for i in df.columns:
        for j in df.index:
                dict_1[i]=df.loc[[i],[j]]
print(dict_1)"""
print(df.to_dict('list'))