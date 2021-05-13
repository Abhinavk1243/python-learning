import pandas as pd
  

"""dict = {'Team':['Arsenal', 'Manchester United', 'Arsenal','Arsenal', 'Chelsea', 'Manchester United','Manchester United', 'Chelsea', 'Chelsea', 'Chelsea'],'Player':['Ozil', 'Pogba', 'Lucas', 'Aubameyang','Hazard', 'Mata', 'Lukaku', 'Morata', 'Giroud', 'Kante'],'Goals':[5, 3, 6, 4, 9, 2, 0, 5, 2, 3] }
df = pd.DataFrame(dict)
#print(df)"""

""""grouping rows
total_goals = df['Goals'].groupby(df['Team'])
print(total_goals)
for i,j in total_goals:
    print(i)
    print(j)"""

#combining multiple column
d = {'id':['1', '2', '3'],
     'Column 1.1':[14, 15, 16],
     'Column 1.2':[10, 10, 10],
     'Column 1.3':[1, 4, 5],
     'Column 2.1':[1, 2, 3],
     'Column 2.2':[10, 10, 10], }
df_1=pd.DataFrame(d)
print(df_1)
group_dict={'Column 1.1':"column1",
     'Column 1.2':"column1",
     'Column 1.3':"column1",
     'Column 2.1':"column1",
     'Column 2.2':"column1"}
df_1= df_1.set_index('id')
df_1= df_1.groupby(group_dict, axis = 1).min()

print(df_1)