import configparser
from loggingconf.log import logger


def getcp():
    cp1 = configparser.ConfigParser()
    logger.info("configparser parse the file config.txt config")
    cp1.read("configurations/config.txt")
    return cp1


cp = getcp()
