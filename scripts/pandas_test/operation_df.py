import pandas as pd 
data1 =  {'F_Name':['Jai', 'Anuj', 'Jai', 'Prince', 'Gaurav', 'Anuj', 'Prince', 'Abhinav'],
          'L_Name':["Singh","Kumar","Singh","Sharma","goel","Kumar","Shrama","Parjapati"],
          'Age':[27, 24, 22, 32, 33, 36, 27, 32],
          'Address':['Nagpur', 'Kanpur', 'Allahabad', 'Kannuaj','Jaunpur', 'Kanpur', 'Allahabad', 'Aligarh'],
          'Qualification':['Msc', 'MA', 'MCA', 'Phd','B.Tech', 'B.com', 'Msc', 'MA'],
          "Weight":[78,45,70,87,68,89,80,47]}
df=pd.DataFrame(data1)

#function 
"""def fun_age(num):
    if num>30:
        return "yes"
    else:
        return "no"
def fun_weight(num):
    if num>=80:
        return "OverWeight"
    elif num<=50: 
        return "Underweight"
    else:
        return "Yes"
df["Age_Eligible"]=df["Age"].apply(fun_age)
df["weight_el"]=df["Weight"].apply(fun_weight)
print(df)
"""
# using lambda
'''df["Mass"]=df["Weight"].apply(lambda x :x/9.8)
print(df)'''

#df["F_Name"]= df["F_Name"].str.join("?")
#print(df)

#2 col to 1 col
df["Name"]=df["F_Name"].str.cat(df["L_Name"],sep=" ")
print(df)