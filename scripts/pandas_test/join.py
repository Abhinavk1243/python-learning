import pandas as pd 
data1 = {'Name':['Jai', 'Princi', 'Gaurav', 'Anuj'], 
        'Age':[27, 24, 22, 32]} 
    
# Define a dictionary containing employee data 
data2 = {'Address':['Allahabad', 'Kannuaj', 'Allahabad', 'Kannuaj'], 
        'Qualification':['MCA', 'Phd', 'Bcom', 'B.hons']} 
  
# Convert the dictionary into DataFrame  
df = pd.DataFrame(data1,index=['K0', 'K1', 'K2', 'K3'])
  
# Convert the dictionary into DataFrame  
df1 = pd.DataFrame(data2, index=['K0', 'K2', 'K3', 'K4'])
#print(df ,'\n\n', df1)

outer = df.join(df1,how='outer')
print(outer)
#inner = df.join(df1,how='inner')


#left = df.join(df1,how='left')
#right = df.join(df1,how='right')

