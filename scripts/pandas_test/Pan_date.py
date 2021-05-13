import pandas as pd 
import datetime as dt
rng=pd.DataFrame()
rng["Lec_date"]=pd.date_range('28/04/2021 09:00:00',periods=5,freq='H')
rng[:5]
#rng['year'] = rng['date'].dt.year
#rng['month'] = rng['date'].dt.month
#rng['day'] = rng['date'].dt.day
#rng['hour'] = rng['date'].dt.hour
#rng['minute'] = rng['date'].dt.minute
#print(rng)
#t=pd._tslib.Timestamp.now()
#print(pd.to_datetime(t))
#rng["Lec_Name"]=["Maths","Physics","Chemistry","IT","English"]
#rng["Teacher_name"]=["Abhinav","Aakash","Abhishek","Abhay","Ayansh"]
"""print(rng)
# Get hour detail from time data
rng['Lec_date'] = pd.to_datetime(rng.Lec_date)
print(rng["Lec_date"].dt.time)
#print(rng.dtypes)"""
ts = pd.Timestamp(year = 2011,  month = 11, day = 21, hour = 23, second = 49, tz = 'US/Central') #making time stamp object

  
# Print the Timestamp object
print(ts)
print(pd.to_datetime(ts))
print(ts.timestamp())
print(ts.replace(year = 2019, month = 12, hour = 1))

#print(ts.now())
#print(ts.isoformat())
#print(ts.date())