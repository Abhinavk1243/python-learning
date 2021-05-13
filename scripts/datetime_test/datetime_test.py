
from datetime import datetime,date,time
import pytz
d=date(2020, 4, 23)
d1=datetime(2021,4,26,16,20,20,312333)
print(d)
print(d1)
print(datetime.date(d1))
print(datetime.time(d1))
print(d1.astimezone(pytz.timezone("America/Los_Angeles")))
print(date.fromtimestamp(132141253))
print(d1.year)
print(d1.month)