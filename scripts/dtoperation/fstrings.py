def my_function(normal,*args,**kwargs):
    print(normal)
    for item in args:
        print(item)
    for key,value in kwargs.items():
        print(f"{key} is {value}")


normal="students of class are"
students=["abhinav","abhishek","akash"]
roles={"monitor":"rohan","head boy":"arpit"}
my_function(normal,*students,**roles)