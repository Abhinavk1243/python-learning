import configparser
parser = configparser.ConfigParser()

parser.read('config.cfg')

#def get_config(section,key):
    #return parser.get(section,key)  

print(parser["Abhinav_mysql"]["host"])
