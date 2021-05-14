#FILE OPERATIONS
import os
continue_1='y'
while continue_1=='y' or continue_1=='Y':
    file_name=input("enter file name")
    choice=int(input("File operation are as follow : \n 1:Read \n 2:append \n 3: check file exist or not \n 4:read some part of file \n 5:read one line of file \n 6: delete file \n 7:overwrites"))
    if choice==1:
        try:
            file=open(f"scripts/pandas_test/csvfiles/{file_name}","r")
            print(file.read())
            file.close()
        except FileNotFoundError as error:
            print(f" error found : {error}")
    elif choice==2:
        try:
            file=open(f"scripts/pandas_test/csvfiles/{file_name}","a")
            ch=input("Enter the content want to wrie in a file")
            file.write(ch)
            file.close()
            file=open(f"scripts/pandas_test/csvfiles/{file_name}","r")
            print(file.read())
            file.close()
        except FileNotFoundError as error:
            print(f" error found : {error}")
    elif choice==3:
        if os.path.exists(f"scripts/pandas_test/csvfiles/{file_name}"):
            print("file exist")
        else:
            print("file does not exist")
    elif choice==4:
        try:
            ch=int(input('enter the number of character want to read'))
            file=open(f"scripts/pandas_test/csvfiles/{file_name}","r")
            print(file.read(ch))
            file.close()
        except FileNotFoundError as error:
            print(f" error found : {error}")
            print("Please write a name of existig file")
    elif choice==5:
        try:
            file=open(file_name,"r")
            print(file.readline())
            file.close()
        except FileNotFoundError as error:
            print(f" error found : {error}")
            print("Please write a name of existig file")
    elif choice==6:
        if os.path.exists(f"scripts/pandas_test/csvfiles/{file_name}"):
            os.remove(f"scripts/pandas_test/csvfiles/{file_name}")
        else:
            print("file does not exist")
    elif choice==7:
        file=open(f"scripts/pandas_test/csvfiles/{file_name}","w")
        ch=input("Enter the content want to wrie in a file")
        file.write(ch)
        file.close()
        file=open(f"scripts/pandas_test/csvfiles/{file_name}","r")
        print(file.read())
        file.close()
    continue_1=input("do you want to continue 'y' or 'Y'")


        

    

