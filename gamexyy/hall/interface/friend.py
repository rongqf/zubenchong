# -*- coding: utf8 -*-

import tornado.web

from lib import userstruct, friendstruct


import time
import random
from lib.log import logger


def handle_getfriend(param):
    ret = 0
    userid = param.get('userid')
    skey = param.get('skey')

    if userid and skey:
        tmp = userstruct.read_redis(userid)
        if not tmp or tmp.skey != skey: 
            return {'ret':0, 'data':{'des': 'skey error'}}

        dbret = friendstruct.get_friend(userid)

        ftmp = []
        for p in dbret:
            p['title'] = userstruct.getusertitle(p['exp'])
        return {'ret':1, 'data': dbret}

    return {'ret':0, 'data': {'des': 'input error'}}

def handle_getfriendreq(param):
    ret = 0
    userid = param.get('userid')
    skey = param.get('skey')

    if userid and skey:
        tmp = userstruct.read_redis(userid)
        if not tmp or tmp.skey != skey: 
            return {'ret':0, 'data':{'des': 'skey error'}}

        dbreq = friendstruct.get_friendreq(userid)
        dbacc = friendstruct.get_friendacc(userid)

        return {'ret':1, 'data': {'req': dbreq, 'acc': dbacc}}

    return {'ret':0, 'data': {'des': 'input error'}}

    
def handle_add(param):
    ret = 0 
    userid = param.get('userid')
    skey = param.get('skey')
    otherusername = param.get('otherusername')

    if userid and skey and otherusername:
        tmp = userstruct.read_redis(userid)
        if not tmp or tmp.skey != skey: 
            return {'ret':0, 'data':{'des': 'skey error'}}

        other = userstruct.read_mysql(otherusername)
        if not other: 
            return {'ret':0, 'data':{'des': 'otherusername error'}}

        logger.debug("%s, %s", userid, other.userid)
        dbret = friendstruct.req_friend(userid, other.userid)
        return {'ret':1, 'data': dbret}

    return {'ret':0, 'data': {'des': 'input error'}}


def handle_accept(param):
    ret = 0
    userid = param.get('userid')
    skey = param.get('skey')
    otherid = param.get('otherid')
    acode = param.get('acode')

    if userid and skey and otherid != None and acode != None:
        tmp = userstruct.read_redis(userid)
        if not tmp or tmp.skey != skey: 
            return {'ret':0, 'data':{'des': 'skey error'}}

        dbret = friendstruct.acc_friend(otherid, userid, acode)
        return {'ret':1, 'data': dbret}

    return {'ret':0, 'data': {'des': 'input error'}}