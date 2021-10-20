import pandas as pd 
from lib import read_config
logger=read_config.logger()

def readcsv(list_df,list_set_col):
    """Method to read csv files 

    Args:
        l (array): list of dataframes 
        list_set_col (set): empty set 

    Returns:
        array: merged dataframe 
    """
    try:
        no_of_df=int(input("enter the number of dataframe"))
        for i in range(no_of_df):
            path=input("enter path of file")
            df1=pd.read_csv(f"scripts/pandas_files/csvfiles/{path}.csv",sep="|")
            list_df.append(df1)
            list_set_col.append(set(df1.columns))
        logger.debug("All csv file was read into a dataframe")
        return list_df
    except FileNotFoundError as e:
        logger.error(f"error arrise :{e}")


# function for merging a csv filesS
def merge_df(list_df,list_set_col):

    """Method to merge number of dataframes

    Args:
        l (array): array that contain dataframes which had to merged
        list_set_col (set): set of list where every list contain column name of respective dataframes

    Returns:
        dataframe : return the final merged dataframe
    """
    try:
        com_col=set()
        for i in range(0,len(list_set_col)):
            if i==0:
                com_col=com_col.union(list_set_col[i])
            else:
                com_col=com_col.intersection(list_set_col[i])
        com_col=list(com_col)
        df=pd.DataFrame()
        counter=0
        for i in list_df:
            if counter==0:
                df=i
                counter=counter+1
            else:
                df=pd.merge(i,df,how="outer",on=com_col).fillna(0)
                
        logger.debug("All dataframe was merged successfully")
        return df
    
    except Exception as e:
        logger.error(f"exception arise : {e}")

#Function to filer 
def filter(df,value,args):
    """Method is use to filter the rows

    Args:
        df4 (Dataframes): dataframe whose row has to be filtered out

    Returns:
        dataframe :  final dataframe after row filtering
    """
    try:
        
        for i in args:
            df=df[df[i] !=value]
        logger.debug(f"Row was filtered which contain : '::unspecified::' ")
        return df
    except Exception as e:
        logger.error(f"exception arise : {e}")

def filter_col_value(df,col_args,value):
    """return df the with row which having value giving as parameter

    Args:
        df (DataFrame): [description]
        col_args (array): [description]
        value (string): [description]

    Returns:
        [type]: [description]
    """
    try:
        for i in col_args:
            df=df[df[i] ==value]
        logger.debug(f"Row was filtered which contain : '::unspecified::' ")
        return df
    except Exception as e:
        logger.error(f"exception arise : {e}")
            
            
 

#function for melt dataframe
def meltdf(df,id_vars,metric_name,metric_value):
    """This function is useful to massage a DataFrame into a format where one or more columns are identifier variables (id_vars), while all other columns, considered measured variables (value_vars), are "unpivoted" to the row axis, leaving just two non-identifier columns, 'variable' and 'value'. 
 
    Args:
        df4 (dataframe): dataframe which has to be melt

    Returns:
        dataframe: unpivoted dataframe
    """
    try:
        df=pd.melt(df,id_vars=id_vars,var_name=metric_name,value_name=metric_value)
        df[metric_value]=df[metric_value].astype(int)
        df=df[df[metric_value]>0]
        logger.debug("dataframe melt")
        return df
    except Exception as e:
        logger.error(f"exception arise : {e}")


#function to save csv file
def savecsv(df,file_name):
    """Method use to save dataframe as .csv file in directories

    Args:
        df4 (dataframe): Dataframe
    """
    try:
        
        df.to_csv(f"scripts/pandas_files/csvfiles/{file_name}.csv",sep="|",index=False)
        logger.debug(f" resulted dataframe saved in {file_name}.csv ")
    except Exception as e:
        logger.error(f"exception arise : {e}")