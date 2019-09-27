# -*- coding: utf8 -*-

import tornado.web

from lib import userstruct

import time
import random
import hashlib
from lib.log import logger

def md5(txt):
    m = hashlib.md5()   
    m.update(txt)
    return m.hexdigest()
    
def handle(param):

    ret = 0
    
    userid = param.get('userid')
    skey = param.get('skey')
    logger.info("%s,%s", userid, skey)

    if userid and skey:
        tmp = userstruct.read_redis(userid)
        if not tmp or tmp.skey != skey: 
            return {'ret':0, 'data':{'des': 'skey error'}}

        userstruct.write_redis_dict(tmp.userid, {})
        
        return {'ret':1, 'data':tmp.todict()}

    return {'ret':0, 'data': {}}