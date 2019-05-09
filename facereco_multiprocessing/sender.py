#-*- coding:utf-8 -*-

import requests


keywords = {"name" : "jack"}
pictures = {"img" : open("/home/jack/Desktop/jack.png")}

url = "http://127.0.0.1:8888/load"

r = requests.post(url, data=keywords, files= pictures)
