import json
import pandas as pd 
import sys

def read_json_file(file_name):
    """Method is used to read json data from .json file

    Args:
        file_name (str): name of json file 

    Returns:
        Python dictonary object: json data converted into python dictonary object
    """
    try:
        f=open(f"scripts\dtoperation\json_files\{file_name}.json",)
        dict_2=json.load(f)  # load file object
        return dict_2
    except Exception as error:
        print(f"error occurs :{error}")
    f.close()

def write_into_json(dict_1,file_name):
    """Method is used to  write data into json file

    Args:
        dict_1 (dictonary): python dictonanry 
        file_name (str): name of file  to which want write 
    """
    try:
        with open(f"scripts\dtoperation\json_files\{file_name}.json","a") as file:
            json.dump(dict_1,file)
    except FileNotFoundError as error:
        print("error occurs :{errors}")
    finally:
        file.close()

def csv_to_json(csvfile_1):
    dict_4=dict()
    df=pd.read_csv(f"scripts\pandas_test\csvfiles\{csvfile_1}.csv")
    dict_4=df.to_dict('list')
    json_1=json.dumps(dict_4)
    return json_1



def main():
    dict_1={"Name":["Abhinav","Abhishek","Aakash"],
            "roll_no":[1,2,3],
            "marks":[89,67,77]
            }

    dict_3=read_json_file("student_detail")
    print(csv_to_json("marks"))
    
if __name__=="__main__":
    main()
