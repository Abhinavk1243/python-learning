import csv
def write_csv():
    """Method used to write in csv
    """
    file_name=input("enter the name of file")
    list_element=input('Enter the element of list')
    list_1=list_element.split(",")
    for i in range(0,len(list_1)):
        if list_1[i].isdigit():
            list_1[i]=int(list_1[i])
    try:
        with open(file_name,'w',newline='') as file:
            writer_1 = csv.writer(file)
            writer_1.writerow(list_1)
            file.close()
    except:
        print("something went wrong while writing")

def read_csv():
    """Method use to read the csv file
    """
    file_name=input("enter the name of file")
    try:
        with open(file_name,'r') as file:
            reader_1=csv.reader((file))
            for row in reader_1:
                print(row)
            file.close()
    except:
        print("No Such file existed")
        print("Please enter correct name ")

def append():
    """Method used to apend the record in a csv file
    """
    file_name=input("enter the name of file")
    list_element=input('Enter the element of list')
    list_1=list_element.split(",")
    for i in range(0,len(list_1)):
        if list_1[i].isdigit():
            list_1[i]=int(list_1[i])
    try:
        with open(file_name,'a',newline='') as file:
            writer_1 = csv.writer(file)
            writer_1.writerow(list_1)
            file.close()
    except:
        print("something went wrong while writing")

def main():
    continue_1="y"
    while continue_1=='y' or continue_1=='Y':
        choice=int(input('choice are: \n 1: read \n 2: write \n 3:append'))
        if choice==1:
            read_csv()
        elif choice==2:
            write_csv()
        elif choice==3:
            append()
        continue_1=input("want to continue 'y' or 'Y' ")

if __name__=="__main__":
    main()