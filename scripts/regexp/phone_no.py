import re
def phone_no_valid(phone_no):
    return re.findall("[0-9]\d{9}",phone_no)

phone_no=input("enter phone number")
if phone_no_valid(phone_no):
    print("yes number is valid")
else:
    print("number is invalid")