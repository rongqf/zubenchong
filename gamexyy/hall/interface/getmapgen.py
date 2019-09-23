# -*- coding: utf8 -*-

import time
import random
from lib.log import logger
from lib import mapstruct
from lib import userstruct

def handle(param):
	ret = 0

	userid = param.get('userid')
	skey = param.get('skey')
	mapdata = mapstruct.MapInfo()
	tmpgen = mapdata.getGenAll()
	if userid and skey:
		tmp = userstruct.read_redis(userid)
		
		if not tmp or tmp.skey != skey: 
			return {'ret':0, 'data':{'des': 'skey error'}}

		mapdata = tmp.getmap()
		logger.info("%s", tmp)
		#time.sleep(3)
		if mapdata:
			tmpgen = mapdata.getGenAll()
		
	return {'ret':ret, 'data':tmpgen}
