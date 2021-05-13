list_1=[1,2,3,0,4,5,6]
dict_1={1:"abhinav",2:"Aakash"}


try:
    input_1=int(input("enter the value"))

except EOFError as error:
    print(f"EOf error exception arrives : {error}")
except ValueError as error:
    print(error)
    

for i in range(0,8):
    try:
        print(input_/list_1[i])
    except RuntimeError as error:
        print(f"Runtime error {error}")
    except  ZeroDivisionError as error:
        print(f"errors arrise : {error}")
    except NameError as error: # error
        print(f"name error : {error}")
    
    except IndexError as error:
        print(f"list out of index error :{error}")
    except Exception as error:
        print(f"hello {error}")

try:
    print(f"value of  third is {dict_1[3]}")
except KeyError as e:
    print(f"exception generated {e}")