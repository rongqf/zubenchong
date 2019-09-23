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

	if userid and skey:
		tmp = userstruct.read_redis(userid)

		if not tmp or tmp.skey != skey: 
			return {'ret':0, 'data':{'des': 'skey error'}}

		mapdata = tmp.getmap()
		logger.debug('%s, %s', mapdata, type(mapdata))
		if not mapdata:
			mapdata = mapstruct.MapInfo()
			userstruct.write_redis_dict(userid, {'mapdata': mapdata.tojson()})

		logger.debug('%s, %s', mapdata, type(mapdata))
		return {'ret':1, 'data':mapdata.todict()}	
	return {'ret':ret, 'data':{}}
