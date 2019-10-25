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

	attackuserid = param.get('attackuserid')
	attackid = param.get('attackid')
	bid = param.get('attackbid')
	if userid and skey and attackuserid and attackid and bid != None:
		tmp = userstruct.read_redis(userid)

		if not tmp or tmp.skey != skey:
			return {'ret':0, 'data':{'des': 'skey error'}}

		if userid == attackuserid:
			return {'ret':0, 'data':{'des': 'not can attac youself'}}

		apoint = mapstruct.getAttacPoint(attackid)
		if apoint <= 0:
			return {'ret':0, 'data': {'des': 'attackid input error'}}

		if tmp.gamepoint < apoint:
			return {'ret':0, 'data': {'des': 'you point not enough'}}

		attackuser = userstruct.read_user(attackuserid)
		if not attackuser:
			return {'ret':0, 'data': {'des': 'attackbid error'}}

		mapdata = attackuser.getmap()
		aret = mapdata.addAttack(bid, attackid)
		if not aret:
			return {'ret':0, 'data': {'des': 'aret error'}}

		logger.info('mapdata:%s, apoint:%s', mapdata, apoint)

		userstruct.write_redis_dict(attackuserid, {'mapdata': mapdata.tojson()})

		rds = rdsmanager.get_client(userid)
		rkey = 'hashuser:%s' % userid
		rds.hincrby(rkey, 'gamepoint', -apoint)

		return {'ret':1, 'data': {'des': 'attac ok'}}

	return {'ret':0, 'data':{'des': 'input error'}}
