import re
def passvalid(pass_1):
    pattern = "/(?=.*\d)(?=.*[a-z])(?=.[A-Z]).{8,16}$/"
    result = re.findall(pattern, password)
    return result

password = input("Enter string to test: ")
if (passvalid(password)):
    print("Valid password")
else:
    print("Password not valid")
