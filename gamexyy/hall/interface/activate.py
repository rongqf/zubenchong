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
			bret = mapdata.activate(bid)
			if bret:
				tmpgen = mapdata.getGenAll()
				userstruct.write_redis_dict(userid, {'mapdata': mapdata.tojson()})
				return {'ret':ret, 'data':tmpgen}
			else:
				return {'ret':ret, 'data': {'des': 'input error'}}
	return {'ret':ret, 'data':{}}
