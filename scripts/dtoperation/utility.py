import argparse
def calc(a):
    return a.num1 + a.num2 + a.const


if __name__=="__main__":
    
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('num1',type=int,help="first number")
    parser.add_argument('num2',type=int,help="second number")
    parser.add_argument('-c',dest="const",type=int,default=23)
    # parser.add_argument('operation',type=str,help="operation performed")
    args = parser.parse_args()
    print(args.num1)
#n1=args.num1
#n2=args.num2
#print(calc(n1,n2))


