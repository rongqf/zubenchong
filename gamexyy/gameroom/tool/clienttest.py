#coding:utf8

import time

from socket import AF_INET,SOCK_STREAM,socket
from thread import start_new
import struct
HOST='localhost'
PORT=1000
BUFSIZE=1024
ADDR=(HOST , PORT)
client = socket(AF_INET,SOCK_STREAM)
client.connect(ADDR)

def sendData(sendstr,commandId):
    HEAD_0 = chr(0)
    HEAD_1 = chr(0)
    HEAD_2 = chr(0)
    HEAD_3 = chr(0)
    ProtoVersion = chr(0)
    ServerVersion = 0
    sendstr = sendstr
    data = struct.pack('!sssss3I',HEAD_0,HEAD_1,HEAD_2,\
                       HEAD_3,ProtoVersion,ServerVersion,\
                       len(sendstr)+4,commandId)
    senddata = data+sendstr
    return senddata

def resolveRecvdata(data):
    head = struct.unpack('!sssss3I',data[:17])
    length = head[6]
    data = data[17:17+length]
    return data

s1 = time.time()

def start():

    for i in xrange(10):
        client.sendall(sendData('asdfe',1))
for i in range(0):
    start_new(start,())

import json

for i in xrange(1):
    tmp = {'userid':666, 'skey':'fad5ae5ac108a30b14629d7ba0dac81f'}
    d = json.dumps(tmp)
    client.sendall(sendData(d,100))
time.sleep(1)

