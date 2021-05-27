import logging as lg 
logger = lg.getLogger(__name__)
logger.setLevel(lg.DEBUG)
formatter = lg.Formatter('%(asctime)s : %(name)s :%(levelname)s : %(funcName)s :%(lineno)d : %(message)s ')


file_handler =lg.FileHandler("logger.log")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)



def add(x,y):
    return x+y
def sub(x,y):
    return x-y
def mul(x,y):
    return x*y
def div(x,y):
    try:
        result=x/y
    except ZeroDivisionError as error:
        logger.error(f"tried to divided  by 0 :{error}")
    else:
        return result

def main():
    x=10
    y=0
    logger.debug(add(x,y))
    logger.debug(sub(x,y))
    logger.debug(mul(x,y))
    logger.debug(div(x,y))

if __name__=="__main__":
    main()