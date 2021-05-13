import re 
def validEmail(email):
    return re.findall('^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$',email)


text=input("enter the mail id")
valid=validEmail(text)
if valid:
    print("email id is valid")
else:
    print("not valid")