#!/python3

# This file is part of can2RNET.

import socket, sys, os, array, threading
from time import *
from fcntl import ioctl
from can2RNET import *


debug = True



def dec2hex(dec,hexlen):  #convert dec to hex with leading 0s and no '0x'
    h=hex(int(dec))[2:]
    l=len(h)
    if h[l-1]=="L":
        l-=1  #strip the 'L' that python int sticks on
    if h[l-2]=="x":
        h= '0'+hex(int(dec))[1:]
    return ('0'*hexlen+h)[l:l+hexlen]


#do very little and output something as sign-of-life
def watch_and_wait():
    started_time = time()
    while threading.active_count() > 0 and rnet_threads_running:
        sleep(0.5)
        print(str(round(time()-started_time,2))+'\tX: '+dec2hex(joystick_x,2)+'\tY: '+dec2hex(joystick_y,2)+ '\tThreads: '+str(threading.active_count()))

#does not use a thread queue.  Instead just sets a global flag.
def kill_rnet_threads():
    global rnet_threads_running
    rnet_threads_running = False


if __name__ == "__main__":
    global rnet_threads_running
    rnet_threads_running = True
    can_socket = opencansocket(0)
    canFrameList = []
    while True:
        cf, addr = can_socket.recvfrom(16)
        canFrame = dissect_frame(cf)
        frameid = canFrame.split('#')[0]
        if not(frameid in canFrameList):
              canFrameList.append(frameid)
              print("added: " + frameid)

        


