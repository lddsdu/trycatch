#-*- coding: utf-8 -*-

import os
import sys
from flask import Flask,render_template,request,Response,send_file
import time
from configurations.cpp import cp
from facerecoModule.facereco import Facereco
from gevent import monkey
from gevent.pywsgi import WSGIServer
from facerecoModule.palistener import PAListener
from multiprocessing import Queue
from loggingconf.log import logger
import signal
# wait the camera to capture the frame
index = 0
# queue = Queue()
facereco = Facereco()
palistener = PAListener(facereco)
palistener.initialize()


# monkey's magic
monkey.patch_all()
app = Flask(__name__)


@app.route('/getvideo')
def get_video():
    """video streaming route"""
    return Response(gen(), mimetype="multipart/x-mixed-replace;boundary=frame")


@app.route('/upload', methods=['GET', 'POST'])
def file_upload():
    return render_template("form.html")


@app.route("/load", methods=['GET', 'POST'])
def file_load():
    try:
        name = request.form.get("name")
        file = request.files.get("img")
        file.save(os.path.join("/home/jack/Desktop/listen/", name+".png"))
    except Exception, e:
        logger.warning(e)
        return "False"
    return "True"


def gen():
    """"gen frames data"""
    while True:
        send = facereco.png_data
        yield (b'--frame\r\n' 
               b'Content-Type: image/png\r\n\r\n' + send + b'\r\n')
        #"""python GEL Lock !!! must need to sleep some time !!!"""
        time.sleep(1.0/12)

def writepid():
    pidfile = cp.get("store", "pidfile_path")
    file = open(pidfile, "w")
    pid = os.getpid()
    file.write(str(pid))
    file.close()


def signal_handler(signum, frame):
    logger.info("pid %d going to terminate!!!" % os.getpid())
    sys.exit(0)

if __name__ == '__main__':
    writepid()
    port = cp.getint("server_dev", "port")
    host = cp.get("server_dev", "host")
    http_server = WSGIServer((host, port), app)
    signal.signal(signal.SIGINT, signal_handler)
    try:
        http_server.serve_forever()
    except Exception, e:
        print e
        logger.info("this server to be killed")
