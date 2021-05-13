import pandas as pd 
def filter(df4):
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
