from typing import Counter
import pandas as pd 
from datetime import datetime

def save_csv():
    df=pd.DataFrame(data={"ID":[1,2,3],
                      "name":["abhinav","Abhishek","Aakash"]})
    df["date"]=datetime.now()
    # df.to_csv(path,index=False,sep="|")
    if "role" in list(df.columns):
        return True
    else:
        return False
    
    
print(save_csv())