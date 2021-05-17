# List Manipulation

list_1=[]

# function to append one list to another list
def add_list():
    """This method append a list to another list

    Returns:
        array : result array after adding
    """
    list_element_1=input('Enter the element of list')
    list_2=list_element_1.split(",")
    return list_1+list_2

# function to repeate elements
def repeatition():
    """Method to repete all element of array

    Returns:
        array : final array
    """
    number_of_time=int(input('Enter the number of repeatetion'))
    return list_1*number_of_time

#function to do slicing
def range_slicing():
    """Method used to return sub array of 
    Returns:
        array : sub array
    """

    start_index=int(input('enter starting index for slicing'))
    end_index=int(input('enter end index for slicing'))
    return list_1[start_index:end_index+1]

# function to insert element at specified location
def insert_at_loc():
    """Method use to insert element in a array at specified location

    Returns:
        array : new array after insertion
    """
    element=input("enter element")
    loc=int(input('Enter the location'))
    if element.isdigit()==True:
        element=int(element)
    list_1.insert(loc,element)
    return list_1


def main():
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

if __name__=="__main__":
    main()


