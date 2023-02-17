import pandas as pd 
from datetime import datetime,timedelta,date
def get_date_list(end,month_range,range_type):
    end=datetime.strptime(end,'%Y-%m-%d')
    if range_type=='monthly':
        list_date=[end.strftime("%Y-%m-%d")]
        first = end.replace(day=1)
        for i in range(month_range-1):
            last_month = first - timedelta(days=1)
            list_date.append(last_month.strftime("%Y-%m-%d"))
            first = last_month.replace(day=1)
    elif range_type=='daily':
        list_date = [(end - timedelta(days=x)).strftime("%Y-%m-%d") for x in range(month_range)]
        
    return  list_date

base='2022-12-31'
date_list=get_date_list(base,15,'monthly')



print(date_list)