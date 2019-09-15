# -*- coding: utf8 -*-

import tornado.web

from lib.RedisManager import rdsmanager
from lib import sqlutil

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
        return {'ret':1, 'desc':'input null'}

    
    tmp = sqlutil.GetOneRecordInfo('userinfo', {'username':username})

    if tmp:
        userid = tmp.get('userid')
        salt = tmp.get('salt')
        #passwd = md5(salt + passwd)
        password = tmp.get('password')
        if passwd == tmp.get('password') and userid:
            rds = rdsmanager.get_client(userid)
            skey = md5('%s%s%s%s' % (username, time.ctime(), salt, random.random()))
            tmp['skey'] = skey
            tmp['update_time'] = time.time()
            rkey = 'hashuser:%s' % userid
            rds.hmset(rkey, tmp)

            
            
            ret = 1
        
    return {'ret':ret, 'data':tmp}
