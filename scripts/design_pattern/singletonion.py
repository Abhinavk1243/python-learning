import random
class GovtSingleton:  
    __instance__ = None  
    def __init__(self):  
        if GovtSingleton.__instance__ is None:  
            GovtSingleton.__instance__ = self  
        else:  
            GovtSingleton.__instance__ = GovtSingleton.get_instance()
            # raise Exception("We can not creat another instance")  
            
  
    @staticmethod  
    def get_instance():  
    # We define the static method to fetch instance  
        if not GovtSingleton.__instance__:  
            GovtSingleton()  
        return GovtSingleton.__instance__  
   
    def get_number(self):
        return random.randint(1,10)
   

def main():
    gover = GovtSingleton()  
    print(f"global instance is : {gover}")  
    
    # print(gover.get_number())
    # print("===============")
    
    obj2  = GovtSingleton()
    print(f"global instance is : {obj2}")  
    # same_gover = GovtSingleton().get_instance()  
    # print(same_gover) 

    # another_gover = GovtSingleton().get_instance()  
    # print(another_gover)  
    

    # new_gover = GovtSingleton()  
    # print(new_gover.get_number()) 
    
if __name__ == "__main__":
    main()