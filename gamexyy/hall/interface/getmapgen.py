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
	mapdata = mapstruct.MapInfo()

	if userid and skey:
		rds = rdsmanager.get_client(userid)
		rkey = 'hashuser:%s' % userid
		tmp = rds.hget(rkey, 'mapdata')
		logger.info("%s", tmp)
		#time.sleep(3)
		if tmp and tmp != '':
			mapdata.updatejson(tmp)
			logger.info(mapdata)
			tmpgen = mapdata.getGenAll()
		
	return {'ret':ret, 'data':tmpgen}
