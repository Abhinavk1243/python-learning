from datetime import datetime,timedelta,date
def data(start_date,end_date):
    format="%Y%m%d"
    l=[]
    d=datetime.strptime(start_date,format)
    e=datetime.strptime(end_date,format)
    days=datetime.date(e)-datetime.date(d)
    print(d)
    d= d.replace(minute=59, hour=23, second=59)
    print(d)
    for i in range(1,days.days+1):
        d= d.replace(minute=0, hour=0, second=0)
        d=d+timedelta(days=1)
        print(d)
        d= d.replace(minute=59, hour=23, second=59)
        print(d)

start_date=input("enter start date")
end_date=input("enter end date")
data(start_date,end_date)

