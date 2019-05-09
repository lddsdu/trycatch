#-*- coding:utf-8 -*-


import pymysql
from person import Person
from loggingconf.log import logger


def add_person_info(name, age, sex, imagepath, serializefile, tablename="steaf"):
    db = pymysql.connect("localhost", "root", "abc", "trycatch", charset="utf8")
    sql = "insert into %s values ('%s', %d, '%s', '%s', '%s')" % (tablename, name, age, sex, imagepath, serializefile)
    logger.info("execute %s " % sql)
    cursor = db.cursor()
    try:
        cursor.execute(sql)
        db.commit()
        return True
    except Exception, e:
        logger.info("an error happend when execute sql %s " % sql)
        db.rollback()
        return False


def select_person_info(tablename="steaf"):
    db = pymysql.connect("localhost", "root", "abc", "trycatch", charset="utf8")
    cursor = db.cursor()
    sql = "select name, image_path, serialize_file from %s ;" % tablename
    logger.info(sql)
    person_list = []
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            person = Person(row[0], row[1], row[2])
            person_list.append(person)
    except:
        logger.info("error when select in db operation")
        return None
    return person_list

