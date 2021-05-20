import pandas as pd
import json
f=open(f"scripts\dtoperation\json_files\intents.json",)

dict_2=json.load(f)  # load file object

l=list(dict_2.keys())

for k in l:
    list_1=dict_2[k]
    df=pd.DataFrame()
    j=0
    for i in list_1:

        df1=pd.DataFrame(i,index=[j])
        df=df.append(df1)
        j=j+1
    print(df)
    print("\n")

    