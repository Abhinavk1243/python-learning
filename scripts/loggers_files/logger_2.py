import logging as lg 
logger = lg.getLogger(__name__)
logger.setLevel(lg.INFO)
formatter = lg.Formatter('%(asctime)s : %(filename)s : %(funcName)s : %(lineno)d : %(levelname)s : %(message)s ')


file_handler =lg.FileHandler("logger_2.log")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


logger.debug("Harmless debug message")
logger.info("this is just an information")
logger.warning("Its a Warning")
logger.error("Did you try to divide by zero")
logger.critical("Internet is down")