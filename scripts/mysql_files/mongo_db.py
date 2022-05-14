from typing import List
import pymongo
from pymongo.message import _Query, insert
import pandas as pd

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
def collection_df(colection,query=None,cols=None):
    record = read_from_db(collection,query=query,cols=cols)
    record_dict = {}
    record_dict_list = []
    for row in record:
        for cols in list(row.keys()):
            if type(row[cols]) == str:
                record_dict[cols]=row[cols]
                
            elif type(row[cols]) == list:
                if type(row[cols][0]) == dict:
                    for i in row[cols]:
                        nested_record = record_dict
                        record_dict.update(i)
                        print(record_dict)
                        
                        
                else:
                    record_dict[cols] = ",".join([str(i) for i in row[cols]])
            
def print_records(record):
    for dict_record in record:
        print(dict_record)
        
def make_col_dict(cols):
    col_dict = {}
    for col in cols:
        if col not in col_dict.keys():
            col_dict[col]=1
    return col_dict

def read_from_db(collection,query = None,cols = None):
    if query == None and cols == None:
        return collection.find().sort("employee_salary",-1)
    elif query == None and cols != None:
        col_dict = make_col_dict(cols)
        return collection.find({},col_dict)
    elif query != None and cols == None:
        return collection.find(query)
    else:
        col_dict = make_col_dict(cols)
        return collection.find(query,col_dict)

def update_data(collection,query,new_val):
    collection.update_one(query, new_val)
    

def insert_document(collection,document):
    if type(document) == list:
        x = collection.insert_many(document)
    elif type(document) == dict:
        x = collection.insert_one(document)
    else:
        print("send valid data")
    
if __name__ == "__main__":
    db = myclient["test_db"]
    collection = db["industary"]
    collection = db["employee"]
    # collection = db["product"]
    
    
    df = pd.DataFrame(list(collection.find({})))
    print(df.to_dict(orient="records"))
    query = {'id':12}
    query = {"id" : {"$eq": 12}}
    
    query = {'product.0.stock_industry':{"$eq":"Business Services"}}
    query = {'product.0.stock_industry':{"$eq":"Business Services"}}
    query = {'product.0.stock_industry':{"$eq":"Business Services"}}
    query = {"id" : {"$eq": 12}}
    # collection_df(collection,query=query)
    # record = read_from_db(collection,query={"id" : {"$eq": 2}},cols = {'product.0':1})
    # print("old record")
    # print_records(record)
        
    """updated"""
    # myquery = {'employee_name': 'Abhinav Kumar'}
    # newvalues = { "$set": { 'id': 25} }
    # update_data(collection,myquery,newvalues)
    # record = read_from_db(collection,query=query)
    # print("updated")
    # print_records(record)
    
    
    """insert"""
    # data = {'id': 26, 'employee_name': {'first_name':"Abhishek","last_name":"Chauhan"},  'employee_age': 22, 'profile_image': ''}
    # try:
    #     insert_document(collection,data)
    
    # except Exception as error:
    #     print(error)
    
    # print("new")
    # record = read_from_db(collection)
    # print_records(record)
    
    # record = col.find()
    # for i in col.find(query,{"_id":0,"id":1,"employee_name":1,'employee_salary': 1}):
    #     print(i)
    
    # for x in col.find({},{'employee_salary': 470600}):
    #     print(x)
    # record = collection.aggregate([{'$group' : {'_id': "$stock industry", 'count' : {'$sum' : 1}}}])
    # # record = collection.aggregate([{'$group' : {'_id': "$id", 'count' : {'$min' : "$employee_salary"}}}])
    
    # record = collection.aggregate([{'$group' : {'_id': "$dept", 'count_dept' : {'$sum' : 1}}}])
    # aggregate([{$group : {"_id" : "$employee_salary", count_for_same_age : {$min : "employee_salary"}}}])
