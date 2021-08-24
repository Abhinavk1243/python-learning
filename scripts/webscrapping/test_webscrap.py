from numpy.lib.npyio import save
import requests
import html5lib
from bs4 import BeautifulSoup
import pandas as pd
from requests.api import get
from requests.models import Response 
from library.csvfileprocessing import savecsv,filter,filter_col_value
import texttable as tt

def get_blog_data():
    URL = "https://realpython.github.io/fake-jobs/"
    r = requests.get(URL)
    soup = BeautifulSoup(r.content, 'html.parser')
    results = soup.find(id="ResultsContainer")
    job=results.find_all("h2",class_="title")
    
    job_elements=results.find_all("div", class_="card-content")
    job_title=[]
    company=[]
    location=[]
    for job_element in job_elements:
        job_title.append(job_element.find("h2", class_="title").text.strip())
        company.append(job_element.find("h3", class_="company").text.strip())
        location.append(job_element.find("p", class_="location").text.strip())
        
    data={"Title":job_title,"Company":company,"Location":location}
    df=pd.DataFrame(data)
    # savecsv(df,'web_scrapping_data')
    print(df)
    
    

def parse_list():
    html_list="""
        <h5>Foods</h5>
        <ol start="50">
           <li>Burger</li>
           <li>Pizza</li>
           <li>noodles</li>
        </ol>
        <h5>Drinks</h5>
        <ol type="I" start="50">
           <li>Colddrink</li>
           <li>IceTea</li>
           <li>Milkshake</li>
        </ol>
        """
    soup=BeautifulSoup(html_list, 'html.parser')
    columns=soup.find_all("h5")
    list_dict={}
    
    datas=soup.find_all("ol")
    
    food=[]
    drink=[]
    
    
    
        
        
def table_webscrap():
    url='https://www.worldometers.info/coronavirus/countries-where-coronavirus-has-spread/'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    data_iter=iter(soup.find_all("td"))
    data=[]
    while True:
        try:
            country=next(data_iter).text
            cases=next(data_iter).text
            deaths=next(data_iter).text
            continents=next(data_iter).text
            
            data.append((
              country,
              continents,
              int(cases.replace(",","")),
              int(deaths.replace(",",""))
            ))
        except StopIteration:
            break
        
    data.sort(key = lambda row: row[1], reverse = True)
    table = tt.Texttable()
 

    table.add_rows([(None, None, None, None)] + data)
    table.set_cols_align(('c', 'c', 'c', 'c')) 
    table.header((' Country ', ' Continent ', ' Deaths ', ' Cases '))
    
    df=pd.DataFrame(data,columns=[' Country ', ' Continent ', ' Deaths ', ' Cases '])
    # print(df)
    
    print(table.draw())
    
            
def covid_stats(url,filter_continent="all"):
    
    
    response=requests.get(url)
    soup=BeautifulSoup(response.content,"html.parser")
    
    cols=[]
    for col in soup.find_all("th"):
        if col.text.strip() not in cols:
            cols.append(col.text.strip())
    content=soup.find_all("tr")
    data=[]
    record=[]
    for index,i in enumerate(content):
        record=[]
        for j in i.find_all("td"):
            record.append(j.text.strip())    
        if len(record)!=0:
            data.append(tuple(record))
    
    
    df=pd.DataFrame(data,columns=cols)
    df=filter(df,"",["Country,Other"])
    df=filter(df,"",["#"])
    df=filter(df,"Total:",["Country,Other"])
    df=df.drop("#",axis=1)
    if filter_continent!="all":
        df=filter_col_value(df,["Continent"],filter_continent)
        df=df.drop("Continent",axis=1)
        savecsv(df,filter_continent+"_covid_data")         
    else:
        savecsv(df,"covid_data")
    
def new_tag():
    html=""" <html>
             <head>
             </head>
             <body>
             <h1>hello</h1>
             <h2>Good bye</h2>
             </body>
             </html>
         """
    soup=BeautifulSoup(html,"html.parser")
    new_tag=soup.new_tag("h3")
    new_tag.string="World"
    soup.html.body.append(new_tag)
    print(soup.prettify)
    
    
def main():
    try:
        # new_tag()
        # get_blog_data()
        url="https://www.worldometers.info/coronavirus/"
        # url="https://newzoo.com/insights/rankings/top-10-countries-by-game-revenues/"
        # url="https://covid19.who.int/table"
        covid_stats(url,filter_continent="North America")
        

    except Exception as error:
        print(error)  
    
    
    
if __name__=="__main__":
    main()