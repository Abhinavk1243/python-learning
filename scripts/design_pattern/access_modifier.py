class Student:
    # Private virables
    __name = None
    __id = None
    __age = None
    
    def __init__(self,name,id,age):
        self.__name = name
        self.__id   = id
        self.__age  = age
    
    # Private method
    def __detail(self):
        print(f"name : {self.__name}\nage :{self.__age}\nid :{self.__id}")
        
    def access_private_method(self):
        self.__detail()

    def __str__(self):
        return "hello this the Student class "
        
class Quadrilateral:
    __side1 = None
    __side2 = None
    __side3 = None
    __side4 = None
    
    def __init__(self,side1,side2,side3,side4):
        self.__side1 = side1
        self.__side2 = side2
        self.__side3 = side3
        self.__side4 = side4
        
    def perimeter(self):
        return self.__side1 + self.__side2 + self.__side3 + self.__side4
        
class Rectangle(Quadrilateral):
    def __init__(self,length,breadth):
        super().__init__(length,breadth,length,breadth)
        
    def area(self):
        return self.__side1 * self.__side2


if __name__ == "__main__":
    try:
        # student = Student("Abhinav",121,22)
        # print(student)
        # print(student.__name)
        # print(student.__detail())
        # student.access_private_method()
        
        rect = Rectangle(2,3)
        print(rect.perimeter())
        
    except Exception as error:
        print(error)
    