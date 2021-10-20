import copy
class Fetch:
    def __init__(self):
        self.instruction = []
        
    def fetching(self):
        print("Fetching instrunction...............")
        for i in range(0,9):
            self.instruction.append(i)
            
class Decode:
    def decode(self):
        print("decoding...............")
        
class Execute:
    def execute(self):
        print("Executing...............")
        
class Processing:
    def __init__(self):
        self.fetch = Fetch()
        self.decode = Decode()
        self.execute = Execute()
        
    def start_processing(self):
        self.fetch.fetching()
        self.decode.decode()
        self.execute.execute()
        
        
if __name__ == "__main__":
    process = Processing()
    process.start_processing()
        
