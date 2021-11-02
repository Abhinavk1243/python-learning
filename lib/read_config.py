import mysql.connector as msc
from mysql.connector import pooling
import logging as lg 
import configparser
from lib import transform
import os

def get_config(section,key,file_name='sqlcred.cfg'):
    """Method use to read the value of key in congfig file i.e .cfg extension file

    Args:
        section (string): section name in cfg file whose value want to read
        key (string): key identification of section whose value want to read

    Returns:
        string: value of corresonding section key
    """
    parser = configparser.ConfigParser()
    parser.read(os.path.join(os.path.expanduser("~"),f'config/{file_name}'))
    return parser.get(section,key)  
 
def mysl_pool_connection(section):
    """Metod is use to connect database with python 

    Returns:
        connection : myslconnection"""
    
    dbconfig={ 
              'host' : get_config(section,"host"),
              'user' : get_config(section,"user"),
              'database':get_config(section,"database"),
              'password' :get_config(section,"password")
            }
    cnxn = pooling.MySQLConnectionPool(pool_name = "Abhinav_mysl_pool",**dbconfig)
    pool_cnxn=cnxn.get_connection()
    return pool_cnxn

def logger():
    logger = lg.getLogger(__name__)
    logger.setLevel(lg.DEBUG)
    formatter = lg.Formatter('%(asctime)s : %(name)s : %(filename)s : %(levelname)s\
                             :%(funcName)s :%(lineno)d : %(message)s ')
    file_handler =lg.FileHandler("scripts\logs_files\logsfile.log")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger

def load_rules(filename):
    with open(filename, mode="r", encoding="utf8") as f:
        etl_rules = [ line.strip() for line in f ]
        return etl_rules
    
    
def mapping(df,filename):
    etl_rules=load_rules(filename)
    for i in etl_rules:
            operation_args=i.split("=>")
            operation=operation_args[0]
            args=operation_args[1].split("|")
            df = getattr(transform, operation)(df,args)
            
    return df
    
# data load
