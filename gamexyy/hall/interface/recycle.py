# -*- coding: utf8 -*-

import tornado.web

from lib.RedisManager import rdsmanager

from lib import userstruct
from lib import sqlutil

import hashlib
import time, re
import random
from lib.log import logger


    
def handle(param):

    ret = 0
    userid = param.get('userid')
    skey = param.get('skey')
    bid = param.get('bid')
    if userid and skey and bid != None:
        tmp = userstruct.read_redis(userid)

        if not tmp or tmp.skey != skey: 
            return {'ret':0, 'data':{'des': 'skey error'}}

        mapdata = tmp.getmap()
        logger.info('mapdata:%s', mapdata)

        if mapdata:
            upoint = mapdata.getRecycle(bid)

            logger.info('%s,%s', upoint, tmp.zbc)

            if upoint > 0 and mapdata.recycle(bid):

                logger.info('change point:%s,%s', tmp.zbc, (tmp.zbc + upoint))

                rds = rdsmanager.get_client(userid)
                rkey = 'hashuser:%s' % userid
                pipe = rds.pipeline()
                pipe.hset(rkey, 'mapdata', mapdata.tojson())
                pipe.hincrbyfloat(rkey, 'zbc', upoint)
                pipe.execute() 

                userstruct.write_redis_updateuser(userid)

                return {'ret':1, 'data':mapdata.todict()}
        
    return {'ret':ret, 'data':{'des': 'input error'}}

       