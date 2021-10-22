from abc import ABCMeta,abstractmethod
import copy

class Shape(metaclass = ABCMeta):
    def __init__(self):
        self.id = None 
        self.type = None
        
    @abstractmethod  
    def area(self):
        pass  
    
    @abstractmethod
    def perimeter(self):
        pass
    
    def get_type(self):
        return self.type  
  
    def get_id(self):  
        return self.id  
  
    def set_id(self, sid):  
        self.id = sid  
  
    def clone(self):  
        return copy.copy(self)  

class Circle(Shape):
    def __init__(self,radius):
        super().__init__()
        self.type = "Circle"
        self.radius = radius
        
    def area(self):
        print("inside circle area method")
        return 3.14 * self.radius * self.radius
    
    def perimeter(self):
        print("Inside preimter method of cirecle")
        return 2 * 3.14 * self.radius

class Square(Shape):
    def __init__(self,side):
        super().__init__()
        self.type = "Square"
        self.side = side
        
    def area(self):
        print("inside square area method")
        return self.side * self.side
    
    def perimeter(self):
        print("Inside preimter method of cirecle")
        return 4 * self.side 
    
class Rectangle(Shape):
    def __init__(self,length,width):
        super().__init__()
        self.type = "Square"
        self.length = length
        self.width = width
        
    def area(self):
        print("inside square area method")
        return self.length * self.width
    
    def perimeter(self):
        print("Inside preimter method of cirecle")
        return 2 * ( self.length + self.width )
    
    
class Shape_cache:
    
    cache = {}
    
    @staticmethod
    def get_area(id):
        shape = Shape_cache.cache[id]
        return shape.area()
    
    @staticmethod
    def get_perimeter(id):
        shape = Shape_cache.cache[id]
        return shape.perimeter()
    
    @staticmethod
    def load():
        circle = Circle(3)
        circle.set_id("1")
        Shape_cache.cache[circle.get_id()] = circle
        
        square = Square(3)
        square.set_id("2")
        Shape_cache.cache[square.get_id()] = square
        
        rectangle = Rectangle(2,3)
        rectangle.set_id("3")
        Shape_cache.cache[rectangle.get_id()] = rectangle
        
    @staticmethod
    def get_clone_obj(id):
        shape_obj = Shape_cache.cache.get(id, None)
        return shape_obj.clone()
        
def main():
    # emp = Employee("Abhinav",23,25000)
    Shape_cache.load()
 
    circle = Shape_cache.get_clone_obj("1")
    print(circle.area())
    print(circle.perimeter())
    print("\n")
    
    square = Shape_cache.get_clone_obj("2")
    print(square.area())
    print(square.perimeter())
    print("\n")
 
    rectangle = Shape_cache.get_clone_obj("3")
    print(rectangle.area())
    print(rectangle.perimeter())
    
if __name__ == "__main__":
    # main()
    import copy
    list_1 = [1,2,[2,3],3]
    # list_2 = copy.copy(list_1)
    list_2 = copy.deepcopy(list_1)
    
    # list_2[0] = "hello"
    
    print(id(list_1[2]) == id(list_2[2]))