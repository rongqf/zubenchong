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
	bid = param.get('bid')
	if userid and skey and bid != None:
		tmp = userstruct.read_redis(userid)

		if not tmp or tmp.skey != skey:
			return {'ret':0, 'data':{'des': 'skey error'}}

		mapdata = tmp.getmap()
		logger.info(mapdata)

		if mapdata:
			upoint = mapdata.getUpgrade(bid)
			if upoint > 0 and tmp.gamepoint > upoint and mapdata.upgrade(bid):

				logger.info('change point:%s,%s', tmp.gamepoint, tmp.gamepoint - upoint)

				rds = rdsmanager.get_client(userid)
				rkey = 'hashuser:%s' % userid
				pipe = rds.pipeline()
				pipe.hset(rkey, 'mapdata', mapdata.tojson())
				pipe.hincrby(rkey, 'gamepoint', -upoint)
				pipe.execute()

				userstruct.write_redis_updateuser(userid)

				return {'ret':1, 'data':mapdata.todict()}
		
	return {'ret':ret, 'data':{'des': 'input error'}}

