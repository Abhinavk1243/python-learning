from bs4 import BeautifulSoup
import requests
from requests.models import default_hooks
from lib.read_config import get_config
import pandas as pd

login = get_config("github","username")
password = get_config("github","password")

data = {'login': login,
        'password': password, 'js-webauthn-support': 'supported', 'js-webauthn-iuvpaa-support': 'unsupported',
        'commit': 'Sign in'}

with requests.session() as sess:
    post_data = sess.get('https://github.com/login')
    html = BeautifulSoup(post_data.text, 'html.parser')
    
    
    data.update(timestamp_secret = html.find("input", {'name':'timestamp_secret'}).get('value'))
    data.update(authenticity_token= html.find("input", {'name':'authenticity_token'}).get('value'))
    data.update(timestamp = html.find("input", {'name':'timestamp'}).get('value'))
    
    #Login
    res = sess.post("https://github.com/session", data=data)

    res = sess.get('https://github.com/Abhinavk1243/flask-learning')
    soup=BeautifulSoup(res.content,"html.parser")
    
    files=soup.find_all("div",class_="Box-row Box-row--focus-gray py-2 d-flex position-relative js-navigation-item")
    file_name=[]
    file_status=[]
    last_commit=[]
    
    for  i in files:
        file_name.append(i.find("div",class_="flex-auto min-width-0 col-md-2 mr-3").text.strip())
        file_status.append(i.find("div",class_="flex-auto min-width-0 d-none d-md-block col-5 mr-3").text.strip())
        last_commit.append(i.find("div",class_="color-text-tertiary text-right").text.strip())
        
    github_data={"File":file_name,"Status":file_status,"Last commit":last_commit}
    
    df=pd.DataFrame(github_data)
    print(df)
    
    
    
    
    