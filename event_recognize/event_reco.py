# -*- coding:utf-8 -*-
import sys
import cv2
import os
import json
import time
import signal
from loggingconf.log import logger
from Camera.Camera import Camera
from configurations.cpp import cp
from  multiprocessing import Queue, Pipe
# trycatch_path = cp.get("caffe", "trycatch_path")
pycaffe_path = cp.get("caffe", "pycaffe_path")
sys.path.insert(0, pycaffe_path)
import caffe


queue = Queue()
pipe = Pipe()
# used to check that if the camera already has 18 frames
readyqueue = Queue()
new_size = (128,171,3)
cv2_new_size = (171,128)
camera = Camera(cp.get("camera_dev", "camera_url"), queue, pipe[0], readyqueue)
frames_store = cp.getboolean("store", "frames_store")


def pred(net, data, camera_mode):
    if camera_mode:
        data = data[:, ::-1, :, :, :]
    if frames_store:
        ndarray2disk(data)
    data = (data - 128.0) * 1.0
    data = data.transpose((0, 4, 1, 2, 3))
    # print data.shape
    net.blobs["data"].data[0] = data
    output = net.forward()
    predict = output["prob"]
    return predict


def ndarray2disk(data):
    n, length, height, width, channel = data.shape
    imagespath = getstrtime()
    logger.info(imagespath)
    imagespath = os.path.join("/home/jack/Desktop/test_cam/", imagespath)
    if not os.path.exists(imagespath):
        os.mkdir(imagespath)
    for i in range(length):
        imagename = "%06d.jpg"% i
        cv2.imwrite(os.path.join(imagespath, imagename), data[0, i, :])


def getstrtime(timestamp=None):
    if not timestamp:
        timestamp = currenttime_s()
    time_local = time.localtime(timestamp)
    dt = time.strftime("%Y-%m-%d_%H:%M:%S", time_local)
    return dt


def currenttime_s():
    t = time.time()
    return int(t)


def stophandler(signum, frame):
    print "receive signal : ", signum
    if signum == 2:
        logger.info("stop this module")
        sys.exit(signum)

# todo change the numpy to json format
def pred2json(pred):
    pass

if __name__ == '__main__':
    pidfilepath = cp.get("store", "pidfile_path")
    pidfile = open(pidfilepath, "w")
    pid = os.getpid()
    pidfile.write(str(pid))
    pidfile.close()
    camera_mode = camera.camera_mode
    # os.chdir(trycatch_path)
    logger.info("load the net")
    network = cp.get("strategy", "net")
    tail = None
    pwd = None
    prototxt = None
    model = None
    if network == "tc_3d":
        tail = network
    elif network == "tc_3d_lstm_res":
        tail = network
    else:
        tail = None

    if not tail:
        logger.warning("the strategy in the config.txt need to be one of tc_3d, tc_3d_lstm_res")
        sys.exit(1)

    pwd = cp.get(network, "pwd")
    prototxt = cp.get(network, "prototxt")
    model = cp.get(network, "model")
    os.chdir(pwd)

    net = caffe.Net(prototxt.encode("utf-8"), model.encode("utf-8"), caffe.TEST)
    logger.info("camera start")
    camera.initialize()

    while True:
        try:
            readyqueue.get_nowait()
            break
        except:
            time.sleep(0.1)

    while True:
        signal.signal(signal.SIGINT, stophandler)
        queue.put("need data")
        data = pipe[1].recv()
        predtag = pred(net, data, camera_mode)
        jsoninfo = json.dumps({"normal": predtag[0][0].item(), "steal": predtag[0][1].item()})
        print "json info %s" % jsoninfo



