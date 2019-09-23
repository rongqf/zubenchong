# -*- coding: utf8 -*-

import tornado.web

from lib import userstruct

import hashlib
import time
import random
from lib.log import logger

def md5(txt):
    m = hashlib.md5()   
    m.update(txt)
    return m.hexdigest()
    
def handle(param):

    ret = 0
    username = param.get('username')
    passwd = param.get('password')
    if not username or not passwd:
        return {'ret':0, 'date': {'desc':'input error'}}
    
    tmp = userstruct.read_mysql(username)
    logger.debug(tmp)
    if tmp and passwd == tmp.password:
        rtmp = userstruct.read_redis(tmp.userid)
        if rtmp:
            tmp = rtmp

        skey = md5('%s%s%s' % (username, time.ctime(), random.random()))
        tmp.skey = skey

        userstruct.write_redis_all(tmp)
        
        logger.debug(tmp)
        return {'ret':1, 'data':tmp.todict()}

    return {'ret':0, 'date': {'desc':'username or password error'}}
