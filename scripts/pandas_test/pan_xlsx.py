import pandas as pd 
#dict={"Name":["abhinav","aakash","abhishek","arpit","Rohan","Maynak"], "roll_no":[1,2,3,4,5,6],"Marks":[76,87,90,55,54,66]}
#df=pd.DataFrame(dict)
#riter = pd.ExcelWriter('Test.xlsx', engine ='xlsxwriter')
#3df.to_excel(writer, sheet_name ='Sheet1')
#writer.save()

df=pd.read_excel("Test.xlsx")
print(df)