import configparser

def getconfig(section,key):
    print("inside get config")
    parser = configparser.ConfigParser()
    parser.read('C:/Users/user/config/sqlcred.cfg')
    return parser.get(section,key)  

    