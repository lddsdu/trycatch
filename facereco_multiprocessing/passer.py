#-*- coding:utf-8 -*-
from flask import Flask,render_template,request,Response,send_file
import urllib2
import time
from gevent import monkey
from gevent.pywsgi import WSGIServer


# monkey's magic
monkey.patch_all()
app = Flask(__name__)


@app.route('/slowstream')
def get_video():
    """video streaming route"""
    return Response(gen(), mimetype="multipart/x-mixed-replace;boundary=frame")


def gen():
    """"gen frames data"""
    while True:
        stream = urllib2.urlopen("http://127.0.0.1:8080/?action=snapshot")
        bytes = stream.read()
        yield (b'--frame\r\n' 
               b'Content-Type: image/png\r\n\r\n' + bytes + b'\r\n')
        #"""python GEL Lock !!! must need to sleep some time !!!"""
        time.sleep(1.0/3)

@app.route("/addperson")
def addperson():
    pass

if __name__ == '__main__':
    port = 8899
    host = "0.0.0.0"
    http_server = WSGIServer((host, port), app)
    try:
        http_server.serve_forever()
    except Exception, e:
        print e
    print ("this server to be killed")