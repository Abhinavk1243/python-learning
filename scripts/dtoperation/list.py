# List Manipulation
def add_list():
    list_element_1=input('Enter the element of list')
    list_2=list_element_1.split(",")
    return list_1+list_2
def repeatition():
    number_of_time=int(input('Enter the number of repeatetion'))
    return list_1*number_of_time
def range_slicing():
    start_index=int(input('enter starting index for slicing'))
    end_index=int(input('enter end index for slicing'))
    return list_1[start_index:end_end_index+1]
def insert_at_loc():
    element=input("enter element")
    loc=int(input('Enter the location'))
    if element.isdigit()==True:
        element=int(element)
    list_1.insert(loc,element)
    return list_1


list_element=input('Enter the element of list')
list_1=list_element.split(",")
for i in range(0,len(list_1)):
    if list_1[i].isdigit():
        list_1[i]=int(list_1[i])
print("1:add_list\n 2:repeatiton \n 3:range_slicing \n 4:insert at location \n 5:Reverse \n 6: sorting")
want_continue="y"
while want_continue=="y" or want_continue=="Y":
    choice=int(input('enter your choice by indexing'))
    if choice==1:
         print(add_list())
    elif choice==2:
        print(repeatition()) 
    elif choice==3:
         print(range_slicing())
    elif choice==4:
        insert_at_loc()
        print(list_1)
    elif choice==5:
        print(list_1.reverse())
    elif choice==6:
        print(list_1.sort)
    want_continue=input("want to continue")

    


