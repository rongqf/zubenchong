# -*- coding: utf8 -*-

import tornado.web

from lib.RedisManager import rdsmanager
from lib import sqlutil

import time
import random


from lib.log import logger
from lib import mapstruct


buildinglevelcfg = {
	2: {
		1: {'timeinterval': 15, 'generate': 10},
		2: {'timeinterval': 15, 'generate': 20},
		3: {'timeinterval': 15, 'generate': 30},
		4: {'timeinterval': 15, 'generate': 40}, 
	},
	3: {
		1: {'timeinterval': 10, 'generate': 11},
		2: {'timeinterval': 10, 'generate': 22},
		3: {'timeinterval': 10, 'generate': 33},
		4: {'timeinterval': 10, 'generate': 44}, 
	},
	5: {
		1: {'timeinterval': 8, 'generate': 13},
		2: {'timeinterval': 8, 'generate': 24},
		3: {'timeinterval': 8, 'generate': 35},
		4: {'timeinterval': 8, 'generate': 46}, 
	},
}


	
def handle(param):

	ret = 0
	
	userid = param.get('userid')
	skey = param.get('skey')
	bid = param.get('bid')

	logger.info("%s,%s", userid, skey)
	
	if userid and skey and bid:
		rds = rdsmanager.get_client(userid)
		rkey = 'hashuser:%s' % userid
		tmp = rds.hget(rkey, 'mapdata')
		logger.info("%s", tmp)

		if tmp and tmp != '':
			mapdata = mapstruct.MapInfo()
			mapdata.updatejson(tmp)
			logger.info(mapdata)
			gentmp = mapdata.getGen(bid)
			if gentmp['genflag']:
				mapdata.updatetime[bid] = time.time()

				logger.info('after:%s', mapdata)
				pipe = rds.pipeline()
				pipe.hset(rkey, 'mapdata', mapdata.tojson())
				pipe.hincrby(rkey, 'gamepoint', gentmp['gen'])
				pipe.execute()

			return {'ret':1, 'data':gentmp}
		
	return {'ret':ret, 'data':{}}
