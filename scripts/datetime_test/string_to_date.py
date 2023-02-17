from datetime import datetime,date
def string_to_date(date_1):
    format='%Y-%m'
    date_1=date.strftime(date_1,format)
    return date_1




date_1="2022-09-30"
print(string_to_date(date_1))
