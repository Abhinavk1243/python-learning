import pandas as pd 
df = pd.DataFrame({"Working_days":["Monday","Tuesday","Wednesday","Thursday","Friday"],"New York":[70,73,69,68,75],"Los Angles":[80,78,74,83,76]})
#print(df)
df1=pd.melt(df,id_vars="Working_days",var_name="City",value_name="employes present")
print(df1)
#df2=df1.pivot(index="Working_days",columns="City",values="employes present")
#print(df1))
#print(df2)

#df3=pd.pivot_table(df1,index="Working_days",columns="City")
#print(df3)