import pandas as pd 


d = {'id':['1', '2', '3'],
     'Column 1.1':[14, 15, 16],
     'Column 1.2':[10, 10, 10],
     'Column 1.3':[1, 4, 5],
     'Column 2.1':[1, 2, 3],
     'Column 2.2':[10, 10, 10], }

df = pd.DataFrame(data=d)
data = df.dtypes

# l= list(df.itertuples(index=False, name=None))

print(data)