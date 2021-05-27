import pandas as pd 


dict={"Name":["abhinav","aakash","abhishek","arpit","Rohan","Maynak"], "roll_no":[1,2,3,4,5,6],"Marks":[76,87,90,55,54,66]}
df=pd.DataFrame(dict)

for i,j in df.iterrows():
   print(tuple(j))
"""for i in df.itertuples():
   i=tuple(i)
   print(f"{i}")"""
   
#for i,j in df.iteritems():
   #print(i)
   #print(j)


#df.to_csv("scripts/pandas_files/csvfiles/marks.csv",index=False)