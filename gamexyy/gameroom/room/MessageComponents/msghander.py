#coding:utf8

from twisted.internet import defer, reactor, threads, task

from room.lib.RedisManager import rdsmanager



import json

msghander = {}
    
def addhander(target):
    try:
        key = int((target.__name__).split('_')[-1])
        if key in msghander:
            exist_target = self._targets.get(key)
            raise "target [%d] Already exists,\
            Conflict between the %s and %s"%(key,exist_target.__name__,target.__name__)
        msghander[key] = target
    finally:
        pass






#################################################################################################

import urllib2
import time
def test():
    print 'testa'
    time.sleep(3)
    print 'testb'
    return 'rrrrrrrrrrrrrrrrrrrrrr'

def calldefer():
    return threads.deferToThread(test)

@addhander
def test_threads_50(sessionid, cmdid, data):
    return calldefer()
    
@addhander
@defer.inlineCallbacks
def test_returnValue_51(sessionid, cmdid, data):
    print 'aaaaaaaaaaaaaaa'
    ret = yield calldefer()
    print 'bbbbbbbbbbbbbbbb'
    defer.returnValue(ret + '111111111111111')
