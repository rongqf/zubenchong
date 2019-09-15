# -*- coding: utf8 -*-

import tornado.web

from lib.RedisManager import rdsmanager
from lib import sqlutil

import time
import random


from lib.log import logger

from lib import mapstruct


	
def handle(param):

	ret = 0
	
	userid = param.get('userid')
	skey = param.get('skey')

	logger.info("%s,%s", userid, skey)
	
	if userid and skey:
		rds = rdsmanager.get_client(userid)
		rkey = 'hashuser:%s' % userid
		mapdata = rds.hmget(rkey, ['map', 'maplevel', 'updatetiime'])
		logger.info("%s", mapdata)

		#time.sleep(3)

		if True or not mapdata:
			mapdata = mapstruct.MapInfo()
			rds.hset(rkey, 'mapdata', mapdata.tojson())

		
			return {'ret':1, 'data':mapdata.todict()}

		
	return {'ret':ret, 'data':{}}
