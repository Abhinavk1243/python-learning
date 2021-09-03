from datetime import datetime
def string_to_date(date_1):
    format='%Y%m%d'
    date_1=datetime.strptime(date_1,format)
    return date_1




date_1="Fri, 20 Aug 2021 02:33:35 -0700 (PDT)"
print(string_to_date(date_1))
