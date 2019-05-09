#-*- coding:utf-8 -*-

from configurations.cpp import cp
import cv2
import time
from loggingconf.log import logger
import numpy as np
import urllib2
from multiprocessing import Process, Queue, Pipe


newsize = (171, 128)

# todo add camera logic when it has 18 frames
class Camera(object):
    # capture set get the configurations from the file of config.txt
    def __init__(self, snapshot_url, queue, pipe, readyqueue):
        self.readyqueue = readyqueue
        self.snapshot = snapshot_url
        self.snapshot = self.snapshot.encode("utf8")
        self.frames = np.zeros((1, 18, 120, 120, 3))
        self.thread = None
        self.already_initialized = False
        self.width = cp.getint("camera_dev", "width")
        self.height = cp.getint("camera_dev", "height")
        # 配置摄像头参数
        # self.cap = cv2.VideoCapture(self.camera_id)
        # self.cap.set(3, self.height)
        # self.cap.set(4, self.width)
        self.sample_rate = cp.getint("camera_dev", "sample_rate")
        m = cp.get("mode", "mode")
        self.show = cp.getboolean("show", "show_frame")
        self.queue = queue
        self.pipe = pipe
        self.interval = 1.0 / int( cp.getint("camera_dev", "interval"))
        if m.strip() == "camera":
            self.camera_mode = True

    def initialize(self):
        if self.already_initialized:
            logger.info("camera"+str(self.camera_id)+" already initialized")
            return
        self.already_initialized = True
        self.thread = Process(target=self.new_process_cap)
        # set camera to be daemon process
        self.thread.daemon = True
        self.thread.start()
        logger.info("the camera already initalized")

    def new_process_cap(self):
        logger.info("the camera thread start")
        buffer = np.zeros((3, 120, 120, 3))
        index = 0
        # todo delete i when in production environment
        i = 0
        already_full = False
        while True:
            ret, frame = self.read()
            if ret and self.show:
                cv2.imshow("video", frame)
                cv2.waitKey(1)
            if not ret:
                logger.warning("can not load a pic from %s" % self.snapshot)
            rframe = cv2.resize(frame, newsize)
            rframe = rframe[8:128, 29:149, :]
            buffer[2 - index, :] = rframe

            if not already_full:
                i += 1
                if i == 18:
                    self.readyqueue.put("ready")
                    already_full = True

            index += 1
            if index == 3:
                # add this buffer to self.frames
                # logger.debug("add buffer to self.frames !!!")
                self.frames[0, 3:18, :, :, :] = self.frames[0, :15, :, :, :]
                self.frames[0, 0:3:, :, :, :] = buffer
                pass_data = True
                try:
                    self.queue.get_nowait()
                except:
                    # do not need any frames in event_reco, this module is on computing
                    pass_data = False
                if pass_data:
                    self.pipe.send(self.frames)
                index = 0
            time.sleep(0.2)

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

    # def _thread_pic(self):
    #     data = np.zeros((1, 18, 120, 120, 3))
    #     thread_pic_path = "/home/jack/Desktop/thread_pic/"
    #     startindex = 1
    #     for imagesfolder in os.listdir(thread_pic_path):
    #         for i in range(18):
    #             framelocation = os.path.join(os.path.join(thread_pic_path, imagesfolder) + "/%06d.jpg" % (i * 2 + startindex));
    #             # print framelocation
    #             logger.info(framelocation)
    #             cv2frame = cv2.imread(framelocation)
    #             cv2.imshow("thread_pic", cv2frame)
    #             time.sleep(0.2)
    #             cv2.waitKey(1)
    #             cv2frame = cv2.resize(cv2frame, newsize)
    #             cv2frame = cv2frame[8:128, 29:149, :]
    #             data[0, i, :] = (cv2frame - 128.0) * 1.0
    #         self.frames = data.copy()

def get_str_time(timestamp=None):
    if not timestamp:
        timestamp = current_time_s()
    time_local = time.localtime(timestamp)
    dt = time.strftime("%Y-%m-%d_%H:%M:%S", time_local)
    return dt


def current_time_s():
    t = time.time()
    return int(t)