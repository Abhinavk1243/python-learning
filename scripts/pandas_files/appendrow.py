import pandas as pd

def append_dfs(df1,df2,df3,new_row):
    """Method append 3 dataframe and also add a new row in data reame

    Args:
        df1 (dateframe) : dateframe_1
        df2 (dateframe) : dateframe_2
        df3 (dateframe) : dateframe_3
        new_row (dateframe) : new row 

    Returns:
        dateframe : resulting dataframe
    """
    
    df1=df1.append(df2)
    df3=df1.append(df3,ignore_index=True)
    df3=pd.concat([new_row,df3]).reset_index(drop=True)
    return df3

def main():
    # Creating the first Dataframe using dictionary
    df1 = pd.DataFrame({"a":[1, 2, 3, 4],"b":[5, 6, 7, 8]})
    
    # Creating the Second Dataframe using dictionary
    df2 = pd.DataFrame({"a":[1, 2, 3],"b":[5, 6, 7]})

    df3 = pd.DataFrame({"a":[1,2,3,5],'b':[3,4,5,6],'c':[1,2,3,4]})

    new_row=pd.DataFrame({"a":3,"b":4,"c":5},index=[0])
    
    print(append_dfs(df1,df2,df3,new_row))

if __name__=="__main__":
    main()


