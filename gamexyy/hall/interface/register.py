# -*- coding: utf8 -*-

import tornado.web

from lib import userstruct
from lib import sqlutil

import hashlib
import time, re
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


    if not re.search(u'^[_a-zA-Z0-9\u4e00-\u9fa5]+$', username):
        return {'ret':0, 'data': {'desc':'username is has (!,@,#,$,%...)'}}

    tmp = userstruct.read_mysql(username)
    logger.debug(tmp)
    if tmp:
        return {'ret':0, 'data': {'desc':'username is exist'}}

    if len(passwd) < 6:
        return {'ret':0, 'data': {'desc':'passwd less 6'}}
    
    ret = sqlutil.InsertIntoDB('userinfo', {'username': 'rqf123456', 'password': '112233', 'salt':'11'})
    if not ret:
        return {'ret':0, 'data': {'desc':'InsertIntoDB error'}}

    return {'ret':1, 'data': {'desc':'ok'}}
