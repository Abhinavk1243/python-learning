def is_member(list_1):
    item=input("enter the number want to know is in list")
    if item.isdigit()==True:
         item=int(item)
    print("{} is in {} : {}".format(item,list_1,item in list_1))
    print("{} is not in {} : {}".format(item,list_1,item not in list_1))




list_element=input('Enter the element of list')
list_1=list_element.split(",")
for i in range(0,len(list_1)):
    if list_1[i].isdigit():
        list_1[i]=int(list_1[i])
is_member(list_1)