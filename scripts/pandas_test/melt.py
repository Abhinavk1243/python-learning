import pandas as pd 

def melt_df(df):
    
    df1=pd.melt(df,id_vars="Working_days",var_name="City",value_name="employes present")
    return df1

def pivot_df(df):
    df2=df.pivot(index="Working_days",columns="City",values="employes present")
    return df2

def main():
    df = pd.DataFrame({"Working_days":["Monday","Tuesday","Wednesday","Thursday","Friday"],"New York":[70,73,69,68,75],"Los Angles":[80,78,74,83,76]})
    df=melt_df(df)
    print(df)
    print(pivot_df(df))

if __name__=="__main__":
    main()