# -*- coding: utf8 -*-

import tornado.web

from lib import userstruct
from lib import sqlutil
import time
import random
import hashlib
from lib.log import logger

def md5(txt):
    m = hashlib.md5()   
    m.update(txt)
    return m.hexdigest()

def handle(param):

	ret = 0
	
	userid = param.get('userid')
	skey = param.get('skey')
	oldpwd = param.get('oldpwd')
	newpwd = param.get('newpwd')

	logger.info("%s,%s", userid, skey)

	if userid and skey and oldpwd:
		tmp = userstruct.read_redis(userid)
		if not tmp or tmp.skey != skey: 
			return {'ret':0, 'data':{'des': 'skey error'}}

		if tmp.password != oldpwd: 
			return {'ret':0, 'data':{'des': 'oldpwd error'}}

		if not userstruct.checkpwdfrt(newpwd):
			return {'ret':0, 'data':{'des': 'newpwd format error'}}
		
		skey = md5('%s%s%s' % (tmp.username, time.ctime(), random.random()))
		tmp.skey = skey
		userstruct.write_redis_dict(userid, {'skey':skey})
		sqlutil.execsqlcommit("UPDATE userinfo SET `password` = '%s' where userid = %s" % (newpwd, userid))

		logger.debug(tmp)
		return {'ret':1, 'data':tmp.todict()}

	return {'ret':0, 'data': {}}