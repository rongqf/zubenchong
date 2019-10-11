# -*- coding: utf8 -*-



import time
import random

from lib.log import logger
from lib import mapstruct
from lib import userstruct
from lib.RedisManager import rdsmanager

	
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
			gentmp = mapdata.getGen(bid)

			logger.info('gentmp:%s', gentmp)
			if gentmp['genflag']:
				mapdata.updatetime[bid] = time.time()


				if gentmp['buildstate'] == 2:
					mapdata.buildstate[bid] = 0

				logger.info('%s,%s', gentmp['buildstate'], mapdata.buildstate[bid])

				mapdata.delAttack(bid)

				logger.info('after:%s', mapdata)

				rds = rdsmanager.get_client(userid)
				rkey = 'hashuser:%s' % userid
				pipe = rds.pipeline()
				pipe.hset(rkey, 'mapdata', mapdata.tojson())
				pipe.hincrby(rkey, 'gamepoint', gentmp['gen'])
				pipe.hincrby(rkey, 'exp', gentmp['gen'])
				pipe.execute()

				userstruct.write_redis_updateuser(userid)

				logger.info('mapdata:%s', mapdata)

				return {'ret':1, 'data':gentmp}
			
			return {'ret':1, 'data':gentmp}
		
	return {'ret':ret, 'data':{}}
