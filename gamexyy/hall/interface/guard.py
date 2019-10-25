# -*- coding: utf8 -*-
from lib.RedisManager import rdsmanager

import time
import random

from lib.log import logger
from lib import mapstruct
from lib import userstruct

    
def handle(param):

    ret = 0
    userid = param.get('userid')
    skey = param.get('skey')

    guardid = param.get('guardid')
    bid = param.get('guardbid')

    if userid and skey and guardid and bid != None:
        tmp = userstruct.read_redis(userid)

        if not tmp or tmp.skey != skey:
            return {'ret':0, 'data':{'des': 'skey error'}}

        apoint = mapstruct.getGuardPoint(guardid)
        if apoint <= 0:
            return {'ret':0, 'data': {'des': 'attackid input error'}}

        if tmp.gamepoint < apoint:
            return {'ret':0, 'data': {'des': 'you point not enough'}}


        mapdata = tmp.getmap()
        aret = mapdata.guard(bid, guardid)
        if not aret:
            return {'ret':0, 'data': {'des': 'aret error'}}

        logger.info('mapdata:%s, apoint:%s', mapdata, apoint)

        rds = rdsmanager.get_client(userid)
        rkey = 'hashuser:%s' % userid
        pipe = rds.pipeline()
        pipe.hset(rkey, 'mapdata', mapdata.tojson())
        pipe.hincrby(rkey, 'gamepoint', -apoint)
        pipe.execute()

        userstruct.write_redis_updateuser(userid)


        return {'ret':1, 'data': {'des': 'attac ok'}}

    return {'ret':0, 'data':{'des': 'input error'}}
       