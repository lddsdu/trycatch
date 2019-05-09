#-*- coding:utf-8 -*-

import face_recognition
from loggingconf.log import logger
import pickle


class Person(object):
    def __init__(self, name, image_path, serialize_file):
        self.name = name
        self.image_path = image_path
        self.serialize_file = serialize_file
        logger.info("person %s %s %s" % (self.name, self.image_path, self.serialize_file))

    def image2encoding(self):
        return self.load_encodings_names(self.image_path)

    def file2encoding(self):
        try:
            image_encoding = pickle.load(open(self.serialize_file))
            logger.debug("serialize_file %s" % self.serialize_file)
            return image_encoding, self.name
        except Exception, e:
            logger.info("error : %s" % e)
            return None, None

    def load_encodings_names(self, imagepath):
        image = face_recognition.load_image_file(imagepath)
        try:
            image_encoding = face_recognition.face_encodings(image)[0]
        except Exception:
            logger.info("can not find a face in this pic %s"%imagepath)
        if len(image_encoding) > 0:
            return image_encoding, imagepath[:-4]
        else:
            return None, None
