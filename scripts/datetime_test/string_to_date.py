from datetime import datetime
def string_to_date(date_1):
    format='%Y%m%d'
    date_1=datetime.strptime(date_1,format)
    return date_1




date_1=input("enter date")
print(string_to_date(date_1))
