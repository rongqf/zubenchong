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
	otherid = param.get('otherid')

	if userid and skey:
		tmp = userstruct.read_redis(userid)

		if not tmp or tmp.skey != skey: 
			return {'ret':0, 'data':{'des': 'skey error'}}

		#myself
		if not otherid:		
			mapdata = tmp.getmap()
			logger.debug('%s, %s', mapdata, type(mapdata))
			if not mapdata:
				mapdata = mapstruct.MapInfo()
				userstruct.write_redis_dict(userid, {'mapdata': mapdata.tojson()})

			logger.debug('%s, %s', mapdata, type(mapdata))
			return {'ret':1, 'data':mapdata.todict()}
		#other	
		else:
			other = userstruct.read_user(otherid)
			if not other:
				return {'ret':0, 'data':{'des': 'otherid error'}}

			mapdata = other.getmap()
			logger.debug('%s, %s', mapdata, type(mapdata))
			if not mapdata:
				mapdata = mapstruct.MapInfo()
				userstruct.write_redis_dict(otherid, {'mapdata': mapdata.tojson()})

			logger.debug('%s, %s', mapdata, type(mapdata))
			return {'ret':1, 'data':mapdata.todict()}


	return {'ret':ret, 'data':{'des': 'skey error'}}
