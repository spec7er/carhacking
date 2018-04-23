#!/python3

# This file is part of can2RNET.

import socket, sys, os, array, threading, curses
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

def init():
    stdscr = curses.initscr()
    if curses.has_colors():
        curses.start_color()
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_YELLOW)
        curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_RED)
        curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_GREEN)
        curses.init_pair(6, curses.COLOR_BLACK, curses.COLOR_YELLOW)
        curses.init_pair(7, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(8, curses.COLOR_BLACK, curses.COLOR_BLACK)
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(1)
    return stdscr

def clean(stdscr):
    curses.nocbreak();
    stdscr.keypad(0);
    curses.echo()
    curses.endwin()

if __name__ == "__main__":
 stdscr = init()
 (h, w) = stdscr.getmaxyx()

 # height, width, y, x
 infos_win = curses.newwin(h, w, 0, 0)
 infos_win.clear()
 infos_win.refresh()

 global rnet_threads_running
 rnet_threads_running = True
 can_socket = opencansocket(0)
 canFrameList = []
 canFrameTime = []
    
 while True:
  cf, addr = can_socket.recvfrom(16)
  canFrame = dissect_frame(cf)
  frameid = canFrame.split('#')[0]
  if not(frameid in canFrameList):
              canFrameList.append(frameid)
              canFrameTime.append(time())
 #             print("added: " + frameid)
  else:
         y = canFrameList.index(frameid)
         canFrameTime[y]=time()
         if y<h:
          font = curses.color_pair(1)
          infos_win.addstr(y,0,canFrame,font)

  for i in range(0,len(canFrameList)):
   if ((time() - canFrameTime[i]) > 0.25) and i<h:
    font=curses.color_pair(7)
    infos_win.addstr(i,0,canFrameList[i],font)
  infos_win.refresh()

        


