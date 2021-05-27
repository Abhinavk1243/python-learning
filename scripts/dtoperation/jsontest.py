import json
import pandas as pd 
import xml.etree.ElementTree as ET
import xmltodict

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
    

def write_into_json(dict_1,file_name):
    """Method is used to  write data into json file

    Args:
        dict_1 (dictonary): python dictonanry 
        file_name (str): name of file  to which want write 
    """
    try:
        with open(f"scripts\dtoperation\json_files\{file_name}.json","w") as file:
            json.dump(dict_1,file)
    except FileNotFoundError as error:
        print("error occurs :{errors}")
    finally:
        file.close()

def csv_to_json(csvfile_1):
    """Method convert csvfile data to json format

    Args:
        csvfile_1 (str): csv file name which data has to be converted

    Returns:
        str : json string
    """
    dict_4=dict()
    df=pd.read_csv(f"scripts\pandas_files\csvfiles\{csvfile_1}.csv")
    dict_4=df.to_dict('list')
    json_1=json.dumps(dict_4)
    return json_1

def createxml():
    root=ET.Element("catalog")
    
    m1=ET.Element("mobile")
    root.append(m1)
    b1=ET.SubElement(m1,"brand")
    b1.text="redmi"
    b2=ET.SubElement(m1,"price")
    b2.text="18000"

    m2=ET.Element("mobile")
    root.append(m2)
    c1=ET.SubElement(m2,"brand")
    c1.text="samsung"
    c2=ET.SubElement(m2,"price")
    c2.text="28000"
    tree=ET.ElementTree(root)
    tree.write("scripts/dtoperation/xml_files/mobile_data.xml")

     
def xml_to_json():
    with open("scripts/dtoperation/xml_files/mobile_data.xml") as xml_file:
      data_dict = xmltodict.parse(xml_file.read())
      xml_file.close()
    j=json.dumps(data_dict)
    return j
    




def main():
    dict_1={
            "students":
              [
                {"Name":"Abhinav kumar",
                 "ID": 1,
                 "course": "B.tech",
                 "percentage" : 77
                },
               {"Name":"Abhishek chauhan",
                 "ID": 2,
                 "course": "B.tech",
                 "percentage" : 80
                },
                {"Name":"Aakash rastogi",
                 "ID": 3,
                 "course": "B.tech",
                 "percentage" : 66
                },
                {"Name":"Arpit sharma",
                 "ID": 4,
                 "course": "B.tech",
                 "percentage" : 96
                }
                ],
            "teachers":
              [
                {
                    "Name":"Sanjay Singh",
                    "ID": 112,
                    "Subject": "Python",
                },
               {
                    "Name":"Manoj Sharma",
                    "ID": 129,
                    "Subject": "Maths",
                },
                {
                    "Name":"Rohit Aggarwal",
                    "ID": 116,
                    "Subject": "Soft computing",
                },

                ]
                
            }

    #dict_3=read_json_file("intents")
    write_into_json(dict_1,"student_detail")
    #print(csv_to_json("marks"))
    #createxml()
    #print(parseXML("scripts/dtoperation/xml_files/mobile_data.xml"))
    #print(xml_to_json())
    #df=pd.DataFrame(dict_3)
    #df.to_csv(f"scripts/pandas_files/csvfiles/intents.csv")

if __name__=="__main__":
    main()
