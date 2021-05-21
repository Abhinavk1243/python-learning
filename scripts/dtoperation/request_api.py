import requests
import pandas as pd
import json

def get_resource(url):
    response=requests.get(url)
    return response.json()

def post_resources(url,data):
    response=requests.post(url,data)
    return response.json()

def delete_resourse(url):
    response=requests.delete(url)
    return response.json()

def update_resources(url,dict_1):
    response=requests.put(url,dict_1)
    return response.json()

def main():
    dict_1={
        "name": "morpheus",
        "job": "leader of all"
    }

    json_data=json.dumps(dict_1)
    #print(post_resources("https://reqres.in/api/users",json_data))
    #print(get_resource("https://reqres.in/api/users?page=2"))
    print(update_resources("https://reqres.in/api/users/2",dict_1))

if __name__=="__main__":
    main()