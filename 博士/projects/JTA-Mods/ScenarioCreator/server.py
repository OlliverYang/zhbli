# -*- coding: UTF-8 -*-
import socket
import sys

import cv2
import numpy as np

import struct

HOST = '172.18.32.31'               # Symbolic name meaning all available interfaces
PORT = 2019              # Arbitrary non-privileged port
s = None
FRAME_WIDTH = 1024
FRAME_HEIGHT = 768


def socketToNumpy(data, sockData):
    k=data.shape[2]
    j=data.shape[1]
    i=data.shape[0]
    sockData = np.fromstring(sockData, np.uint8)
    data = np.tile(sockData, 1).reshape((i,j,k))

    return data

for res in socket.getaddrinfo(HOST, PORT, socket.AF_INET,
                              socket.SOCK_STREAM, 0, socket.AI_PASSIVE):
    af, socktype, proto, canonname, sa = res
    try:
        s = socket.socket(af, socktype, proto)
    except socket.error as msg:
        s = None
        continue
    try:
        s.bind(sa)
        s.listen(1)
    except socket.error as msg:
        s.close()
        s = None
        continue
    break
if s is None:
    print('could not open socket')
    sys.exit(1)
conn, addr = s.accept()
print('Connected by', addr)

running = True
counter = 0
waiting_color = True
while running:
    i, ptr = (0,0)
    color = np.zeros((FRAME_HEIGHT, FRAME_WIDTH, 3), np.uint8)
    color_size = color.size
    print('color_size:', color_size)
    mask = np.zeros((FRAME_HEIGHT, FRAME_WIDTH, 1), np.uint8)
    mask_size = mask.size
    print('mask_size:', mask_size)
    imgSize = color.size
    sockData = b''
    result = True

    if waiting_color:
      
      while color_size:
        nbytes=conn.recv(color_size)
        if not nbytes: break; result = False
        sockData+=nbytes
        color_size-=len(nbytes)
        waiting_color = False
      print('received color bytes')
      
      if result:
        counter += 1
        color = socketToNumpy(color, sockData)
        color = (1 - color) * 255  # 1 - 很重要
        color = color[...,[2,1,0]]  # 顺序很重要
        cv2.imwrite('{}.jpg'.format(counter), color)
        conn.sendall(bytes("got_color", "utf-8"))
      else:
        print('stop running')
        running = False
    
    else:
      while mask_size:
        nbytes=conn.recv(mask_size)
        if not nbytes: break; result = False
        sockData+=nbytes
        mask_size-=len(nbytes)
        waiting_color = True
      print('received mask bytes')
      
      if result:
        mask = socketToNumpy(mask, sockData)
        cv2.imwrite('{}.png'.format(counter), mask)
        conn.sendall(bytes("got_mask", "utf-8"))
      else:
        print('stop running')
        running = False

conn.close()
