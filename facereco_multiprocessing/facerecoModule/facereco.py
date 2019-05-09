#-*- coding:utf-8 -*-

import logging
from configurations.cpp import cp
import cv2
import face_recognition
import os
import threading
import numpy as np
from utils.pngutils import numpy2png
from loggingconf.log import logger
import time
from dbutils.dboperate import select_person_info
from multiprocessing import Process, Queue
from PIL import Image, ImageDraw, ImageFont
from testzhongwen import drawtext
import urllib2
stopTag = False


class Facereco():

    def __init__(self):

        # some default initialize
        self.face_frame = None
        self.thread = None
        self.already_initialized = False
        self.folder_path = None
        self.known_face_encodings = None
        self.known_face_names = None
        self.process_this_frame = True
        self.snapshot = cp.get("camera_dev", "snapshot")
        self.camera_id = cp.get("camera_dev", "camera_id")
        self.show = cp.getboolean("show", "show_frame")
        try:
            self.camera_id = int(self.camera_id)
            logger.info("camera_id = %d" % self.camera_id)
        except Exception:
            logger.info("camera_url = %s" % self.camera_id)

        width = cp.getint("camera_dev", "width")
        height = cp.getint("camera_dev", "height")
        # 配置摄像头参数
        self.cap = cv2.VideoCapture(self.camera_id)
        self.cap.set(3, height)
        self.cap.set(4, width)
        self.png_data = None
        self.initialize()

    def read(self):
        """
        get frames form the url    self.snaphsot!!!
        """
        stream = None
        bytes = None
        try:
            stream = urllib2.urlopen(self.snapshot)
            bytes = stream.read()
        except Exception, e:
            logger.info("error handing the url % s" % self.snapshot)
            return False, None

        try:
            i = cv2.imdecode(np.fromstring(bytes, dtype=np.uint8), flags=1)
            return True, i
        except Exception, snapshoterror:
            logger.warning("check get %s" % self.snapshot)
            return False, None

    # two strategy to load face encodings
    def load_Encodings_Names_via_folderpath(self, folder_path):
        known_face_encodings = []
        known_names = []
        for file in os.listdir(folder_path):
            if file.endswith(".txt"):
                continue
            logging.debug("load image " + file)
            image = face_recognition.load_image_file(os.path.join(folder_path, file))
            image_encoding = face_recognition.face_encodings(image)[0]
            if len(image_encoding) > 0:
                known_face_encodings.append(image_encoding)
                known_names.append(file[:-4])
        return known_face_encodings, known_names

    def load_encoding_names_via_database(self):
        person_list = select_person_info()
        known_face_encodings = []
        known_names = []
        if person_list:
            for person in person_list:
                encoding, name = person.file2encoding()
                if not name:
                    logger.warning("CAN NOT FIND A SERALIZED FILE %s" % person.serialize_file)
                    continue
                known_names.append(name)
                known_face_encodings.append(encoding)
                logger.info("add a person %s" % name)
        else:
            logger.info("can not load a person")
        return known_face_encodings, known_names

    def initialize(self):
        self.folder_path = cp.get("facereco_dev","folder_path")
        self.already_initialized = True
        logging.info("need to load the face image and encoding the face to a ndarray,this may need some time")
        self.known_face_encodings,self.known_face_names = self.load_encoding_names_via_database()
        logging.info("success load all images of known people")
        self.start_thread()

    def start_thread(self):
        self.thread = threading.Thread(target=self._thread)
        self.thread.setDaemon(True)
        self.thread.start()

    def _thread(self):
        """
        开启人脸识别的线程
        """
        pass_this_frame = False
        while True:
            ret, frame = self.read()
            if not ret:
                try:
                    logger.warning("cannot get frames from %s " % self.camera_id)
                except:
                       logger.warning("cannot get frames from %d " % self.camera_id)
                continue
            # frame = cv2.resize(frame, (160, 120))
            pass_this_frame = not pass_this_frame
            if not pass_this_frame:
                continue
            rgb_frame = frame[:, :, ::-1]
            small_rgb_frame = cv2.resize(rgb_frame, (0, 0), fx = 0.5, fy = 0.5)
            face_locations = face_recognition.face_locations(small_rgb_frame, model="cnn")
            face_encodings = face_recognition.face_encodings(small_rgb_frame, face_locations)
            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                #	print self.known_face_encodings
                #	print face_encoding
                matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding, tolerance=0.45)
                name = "Unknown"
                if True in matches:
                    first_match_index = matches.index(True)
                    name = self.known_face_names[first_match_index]
                cv2.rectangle(frame, (left * 2, top * 2), (right * 2, bottom * 2), (0, 0, 255), 2)
                cv2.rectangle(frame, (left * 2, bottom * 2- 35), (right * 2 , bottom * 2), (0, 0, 255), cv2.FILLED)
                frame = drawtext( (left * 2  + 6, bottom * 2  - 30), name, 28, (0, 0, 0), frame)
            if self.show:
                cv2.imshow('Video', frame)
                cv2.waitKey(1)

            self.face_frame = frame
            self.png_data = numpy2png(self.face_frame)

            # try:
            #     name, encoding = self.queue.get_nowait()
            #     self.known_face_names.append(name)
            #     self.known_face_encodings.append(encoding)
            # except:
            #     pass
        if self.show:
            cv2.destroyAllWindows()
