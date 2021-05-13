import pandas as pd 
dict={"Name":["abhinav","aakash","abhishek","arpit","Rohan","Maynak"], "roll_no":[1,2,2,4,5,6],"Marks":[76,87,90,55,54,66]}
df=pd.DataFrame(dict)
# print(df)  #print dataframe
#print(df.head(5)) # print dateframe to 5th raw from top
#print(df.tail(3))  #print dataframe to 3rd row from bottom 
#print(df.to_numpy()) # convert data frame to numpy array
  
# dealing with columns
#print(df.loc[:,["Name","Marks"]]) #print selecteed columns
#print(df.drop("Name",axis=1)) # drop column from dataframe
#df.loc[[0,1,3],["pass"]]="yes"
#print(df)

# dealing with rows
#print(df.loc[[2,4,5],:]) #print selecteed columns
#print(df.drop(1,axis=0)) # drop column from dataframe
#new_row=pd.DataFrame({"Name":'Varun',"roll_no":16,"Marks":54},index=[0])# add new row
#df=pd.concat([new_row,df])

#print(df)
#print(df.drop([0,1,2])) #delete row
#print(df.iloc[[2,4],[1,2]]) # view row and column with using iloc

#print(df.loc[(df["Marks"]<70) & (df["Marks"]>55)])
df.loc[[0],[0]]=654
print(df)
print(df.rename(columns={0:"hello"}))
#print(df.isnull())
#print(df[0].isnull())
#print(df['Name'].isnull())
#print(df.dropna(how="any"))
#print(df.truncate(before=3, after=5,axis=0))
#print(df.drop_duplicates(subset=['roll_no'],keep='first'))

"""df.loc[[0],[0]]=67
print(df)
print(df.fillna(34))
"""
#col=list(df)
#for i in col:
 # print(df[i][2])