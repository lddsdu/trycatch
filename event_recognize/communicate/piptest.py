# -*- coding:utf-8 -*-

from multiprocessing import Process, Pipe
import numpy as np
#pip can alse transfor numpy.ndaray


def proc1(pipe):
    s = np.zeros((1, 2, 3, 4))
    # s = "10086"
    pipe.send(s)
    # pipe.send("1")
    # pipe.send("2")



def proc2(pipe):
    a = pipe.recv()
    print a
    pipe.recv()


if __name__ == '__main__':
    pipe = Pipe()
    p1 = Process(target=proc1, args=(pipe[1],))
    p2 = Process(target=proc2, args=(pipe[0],))
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    print '\nend all process',