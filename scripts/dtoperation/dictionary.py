def add_data():
    """This method add key,value pair in a specified dictonary

    Returns:
        Dictonary : dictonary having a new key , value pair added
    """
    key=input("enter the key")
    if key.isdigit()==True:
        key=int(key)
    value=input("enter the value")
    if value.isdigit()==True:
        value=int(value)
    _dict.update({key:value})
    return _dict
def delete_element():
    """This method delete the speified key value pair from dictonary

    Returns:
        Dictonary :  dictonary after deletion of key,value pair
    """
    key=input("enter the key of data which want to delete")
    if key.isdigit()==True:
        key=int(key)
        _dict.pop(key)
        return _dict



_dict=dict()
print("1:add_data \n 2: delete data \n 3: Get keys \n 4: get Values")
want_continue="y"
while want_continue=="y" or want_continue=="Y":
    choice=int(input('enter your choice by indexing'))
    if choice==1:
        print(add_data())
    elif choice==2:
        print(delete_element())
    elif choice==3:
        print(_dict.keys())
    elif choice==4:
        print(_dict.values())
    want_continue=input("want to continue")
    

