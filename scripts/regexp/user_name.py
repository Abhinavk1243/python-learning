import configparser
parser = configparser.ConfigParser()

parser.read('config.cfg')

#def getconfig(section,key):
    #return parser.get(section,key)  

print(parser["Abhinav_mysql"]["host"])
