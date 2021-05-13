import pandas as pd
  
# Creating the first Dataframe using dictionary
df1 = pd.DataFrame({"a":[1, 2, 3, 4],"b":[5, 6, 7, 8]})
  
# Creating the Second Dataframe using dictionary
df2 = pd.DataFrame({"a":[1, 2, 3],"b":[5, 6, 7]})

df3 = pd.DataFrame({"a":[1,2,3,5],'b':[3,4,5,6],'c':[1,2,3,4]})

new_row=pd.DataFrame({"a":3,"b":4,"c":5},index=[0])
#print(df1.append(df2))
#print(df1.append(df2,ignore_index=True))
print(df1.append(df3,ignore_index=True))

#df3=pd.concat([new_row,df3]).reset_index(drop=True)
#print(df3)