import csv
def write():
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

def read():
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
    file_name=input("enter the name of file")
    list_element=input('Enter the element of list')
    list_1=list_element.split(",")
    for i in range(0,len(list_1)):
        if list_1[i].isdigit():
            list_1[i]=int(list_1[i])
    try:
        with open(file_name,'a',new ine='') as file:
            writer_1 = csv.writer(file)
            writer_1.writerow(list_1)
            file.close()
    except:
        print("something went wrong while writing")


continue_1="y"
while continue_1=='y' or continue_1=='Y':
    choice=int(input('choice are: \n 1: read \n 2: write \n 3:append'))
    if choice==1:
        read()
    elif choice==2:
        write()
    elif choice==3:
        append()
    continue_1=input("want to continue 'y' or 'Y' ")

