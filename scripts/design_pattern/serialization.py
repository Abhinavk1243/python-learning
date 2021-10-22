import pickle


from scripts.design_pattern.gettersetter import rectangle

class Pickling:
    def __init__(self,filename):
        self.file_name = filename 
     
    def serialize(self,obj_list):
        file_obj = open(self.file_name,"ab")
        # for obj in obj_list:
        pickle.dump(obj_list,file_obj)
        file_obj.close()
        
    def deserialize(self):
        file_obj = open(self.file_name,"rb")
        obj_list= []
        while True:
            try:
                obj_list.append(pickle.load(file_obj))
  
            except EOFError:
                print("Completed reading details")
                break
        file_obj.close()
        return obj_list
    
    # def update_details(self):
        
    #     f1 = open("test.txt", "rb+")
    #     travelList = []
    #     print("For a example i will be updating only Buses details")
    #     # t_code = int(input("Enter the travel code for the updation: "))
        
    #     while True:
    #         try:
    #             L = pickle.load(f1)
    #             # if L[0] == t_code:
    #             #     buses = int(input("Enter the number Buses ..."))
    #             #     L[3] = buses
    #             travelList.append(L)
    #         except EOFError:
    #             print("Completed Updating details")
    #             break
                
    #     f1.seek(0)
    #     f1.truncate()
        
    #     for i in range(len(travelList)):
    #         pickle.dump(travelList[i], f1)
    #     else:
    #         f1.close()
    
    
    # def read_file(self):
        
    
if __name__ == "__main__":
    # rect = Shape()
    list_cars = ["BMW","Audi","maruti"]
    list_fruits = ["Apple","grapes"]
    
    pkl = Pickling("test.pkl")
    pkl.serialize(list_cars)
    pkl.serialize(list_fruits)
    obj = pkl.deserialize()
    print(obj)