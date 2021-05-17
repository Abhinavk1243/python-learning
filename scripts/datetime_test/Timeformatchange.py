from datetime import datetime
def time_formatChange(date_1):
    date_1=datetime.strptime(date_1,'%Y%m%d')
    date_2=date_1.strftime('%m%Y%d')
    date_2=datetime.strptime(date_2,'%m%Y%d')
    print(date_2)


def main():
    date_1=input("enter date")
    time_formatChange(date_1)

if __name__=="__main__":
    main()
