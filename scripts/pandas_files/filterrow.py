import pandas as pd 
def filter(df4):
    """Method is use to filter the rows

    Args:
        df4 (Dataframes): dataframe whose row has to be filtered out

    Returns:
        dataframe :  final dataframe after row filtering
    """
    filter_value=input("enter the value which u want to use to filter row")
    for i in df4.columns:
        df4=df4[df4[i] !=filter_value]
    return df4

def main():
    df=pd.DataFrame({"Name":["abhinav","aakash","abhishek","arpit","Rohan","Maynak"],
                     "roll_no":[1,2,2,4,5,6],
                     "Marks":[76,87,90,30,54,66]
    })
    print(filter(df))

if __name__=="__main__":
    main()
