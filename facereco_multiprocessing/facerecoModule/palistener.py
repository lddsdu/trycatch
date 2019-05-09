# -*- coding: utf-8 -*-
from configurations.cpp import cp
from loggingconf.log import logger
import face_recognition
import os, shutil
import time
from dbutils.dboperate import add_person_info
from multiprocessing import Process, Pipe, Queue
import pickle
import math
from  threading import Thread


class PAListener(object):
    def __init__(self, facereco):
        self.facereco = facereco
        self.listen_folder = cp.get("folder", "listen_f")
        self.target_folder = cp.get("folder", "target_f")
        self.ser_folder = cp.get("folder", "ser_f")
        self.initialized = False

    def initialize(self):
        if self.initialized:
            logger.info("palistener already start")
        else:
            self.initialized = True
            logger.info("ready to start palistener")
        process = Thread(target=self._process, args=())
        logger.info("face add listener thread start")
        process.setDaemon(True)
        process.start()

    def _process(self):
        format_tail = ".png"
        while True:
            ret = self.check_is_new()
            if ret:
                for one_p in ret:
                    tag, face_encoding, face_name = self.load_encodings_names(one_p)
                    if tag:
                        self.add_person_info(face_name, face_encoding)
                        serialize_file = self.serialize_encoding_2_file(face_encoding, face_name)
                        add_person_info(face_name, 0, 'm',
                                        os.path.join(self.target_folder, one_p),
                                        serialize_file)
                        logger.info("add a person %s " % face_name)
                    else:
                        logger.info("not find a face, will remove this image to /tmp/ dir!")
                    if not tag:
                        shutil.move(os.path.join(self.listen_folder, one_p),
                                    os.path.join("/tmp/", one_p))
                    else:
                        shutil.move(os.path.join(self.listen_folder, one_p),
                                os.path.join(self.target_folder, one_p))
            else:
                time.sleep(0.5)

    def serialize_encoding_2_file(self, face_encoding, face_name):
        filename = face_name + ".ser"
        filename = os.path.join(self.ser_folder, filename)
        with open(filename, "wb") as ser_file:
            pickle.dump(face_encoding, ser_file)
        return filename

    def check_is_new(self):
        someone = os.listdir(self.listen_folder)
        if len(someone) > 0:
            return someone
        else:
            return None

    def load_encodings_names(self, imagepath):
        image = face_recognition.load_image_file(os.path.join(self.listen_folder, imagepath))
        try:
            face_locations = face_recognition.face_locations(image)
            face_location = self.max_face_location(face_locations)
            image_encoding = face_recognition.face_encodings(image, face_location)[0]
        except Exception, e:
            logger.info(str(e))
            logger.info("can not find a face in this pic %s" % imagepath)
            image_encoding = []
        if len(image_encoding) > 0:
            return True, image_encoding, imagepath[:-4]
        else:
            return False, None, imagepath[:-4]

    def max_face_location(self, face_locations):
        max_index = 0
        max_face = 0
        current_index = 0
        for face_location in face_locations:
            current_face = abs(face_location[0] - face_location[2])
            if current_face > max_face:
                max_face = current_face
                max_index = current_index
            current_index += 1
        return [face_locations[max_index],]

    def add_person_info(self, name, encoding):
        """"trans name encoding"""
        self.facereco.known_face_names.append(name)
        self.facereco.known_face_encodings.append(encoding)
