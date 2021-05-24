import pandas as pd 


def readcsv(l,set_list):
    """Method to read csv files 

    Args:
        l (array): list of dataframes 
        set_list (set): empty set 

    Returns:
        array: merged dataframe 
    """
    try:
        n=int(input("enter the number of dataframe"))
        for i in range(0,n):
            path=input("enter path of file")
            df1=pd.read_csv(f"scripts/pandas_test/csvfiles/{path}.csv",sep="|")
            l.append(df1)
            set_list.append(set(df1.columns))
        return l
    except FileNotFoundError as e:
        print(f"error arrise :{e}")


# function for merging a csv filesS
def merge_df(l,set_list):

    """Method to merge number of dataframes

    Args:
        l (array): array that contain dataframes which had to merged
        set_list (set): set of list where every list contain column name of respective dataframes

    Returns:
        dataframe : return the final merged dataframe
    """
    try:
        com_col=set()
        for i in range(0,len(set_list)):
            if i==0:
                com_col=com_col.union(set_list[i])
            else:
                com_col=com_col.intersection(set_list[i])
        list_1=list(com_col)
        df=pd.DataFrame()
        for i in range(0,len(l)):
            if i==0:
                df=pd.merge(l[0],l[1],how="outer",on=list_1).fillna(0)
            if i==1:
                continue
            else:
                df4=pd.merge(l[i],df,how="outer",on=list_1).fillna(0)
        return df4
    except Exception as e:
        print(f"exception arise : {e}")

#Function to filer 
def filter(df4):
    """Method is use to filter the rows

    Args:
        df4 (Dataframes): dataframe whose row has to be filtered out

    Returns:
        dataframe :  final dataframe after row filtering
    """
    try:
        filter_value=input("enter the value which u want to use to filter row")
        for i in df4.columns:
            df4=df4[df4[i] !=filter_value]
        return df4
    except Exception as e:
        print(f"exception arise : {e}")


#function for melt dataframe
def meltdf(df4):
    """This function is useful to massage a DataFrame into a format where one or more columns are identifier variables (id_vars), while all other columns, considered measured variables (value_vars), are "unpivoted" to the row axis, leaving just two non-identifier columns, 'variable' and 'value'. 
 
    Args:
        df4 (dataframe): dataframe which has to be melt

    Returns:
        dataframe: unpivoted dataframe
    """
    try:
        df4=pd.melt(df4,id_vars=["datetime","datetime_friendly","prop28","prop31","prop16","prop8"],var_name="metric_name",value_name="metric_value")
        df4["metric_value"]=df4["metric_value"].astype(int)
        df4=df4[df4.metric_value>0]
        return df4
    except Exception as e:
        print(f"exception arise : {e}")


#function to save csv file
def savecsv(df4):
    """Method use to save dataframe as .csv file in directories

    Args:
        df4 (dataframe): Dataframe
    """
    try:
        file_name=input("Enter name want to save as .csv")
        df4.to_csv(f"scripts/pandas_test/csvfiles/{file_name}",sep="|",index=False)
    except Exception as e:
        print(f"exception arise : {e}")