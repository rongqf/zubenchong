# -*- coding: utf8 -*-

import time
import random
from lib.log import logger
from lib import mapstruct
from lib import userstruct

def handle(param):
	ret = 1

	userid = param.get('userid')
	skey = param.get('skey')
	otherid = param.get('otherid')

	mapdata = mapstruct.MapInfo()
	tmpgen = mapdata.getGenAll()
	if userid and skey:
		tmp = userstruct.read_redis(userid)
		
		if not tmp or tmp.skey != skey: 
			return {'ret':0, 'data':{'des': 'skey error'}}

		if not otherid:
			mapdata = tmp.getmap()
			logger.info("%s", tmp)
			if mapdata:
				tmpgen = mapdata.getGenAll()
		else:
			other = userstruct.read_user(otherid)
			if not other: 
				return {'ret':0, 'data':{'des': 'otherid error'}}

			mapdata = other.getmap()
			logger.info("%s", tmp)
			if mapdata:
				tmpgen = mapdata.getGenAll()

		
	return {'ret':ret, 'data':tmpgen}
