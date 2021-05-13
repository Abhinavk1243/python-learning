from datetime import datetime
t=datetime.now()
print(t)
print("in string is -")
d=t.strftime('%d-%b-%Y (%H:%M:%S.%f)')
print(d)