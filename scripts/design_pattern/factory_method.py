class Course:
    batches = 0
    fees = 0
    duration = ""
    def get_detail(self):
        return self.batches,self.fees,self.duration
    
class Python(Course):
    batches = 2
    fees = 5000
    duration = "4 months"
    
class Java(Course):
    batches = 3
    fees = 7000
    duration = "6 months"

class Php(Course):
    batches = 2
    fees = 4000
    duration = "5 months"    
    
class ButtonFactory():
    def create_button(self, typ):
        targetclass = typ.capitalize()
        return globals()[targetclass]()
    
if __name__ == "__main__":
    button_obj = ButtonFactory()
    button = ["java", "python","php"]
    
    for i in button:
        batches,fees,duration = button_obj.create_button(i).get_detail()
        print(f" {i} course detail :\n batches : {batches} \n fees : {fees} \n duration : {duration}")