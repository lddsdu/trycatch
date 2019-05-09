import os
import signal
from configurations.cpp import cp
from loggingconf.log import logger


pidfile = cp.get("store", "pidfile_path")
try:
    file = open(pidfile, "r")
except:
    logger.info("pidfile not exists")

pid = file.read()
file.close()

pid = int(pid)

try:
    os.kill(pid, signal.SIGINT)#interrupt  zhongduan
    logger.info("will stop the process of %d." % pid)
    print "kill success"
except OSError, e:
    logger.info("a error happend when kill the process %d" % pid)
    print "kill error"