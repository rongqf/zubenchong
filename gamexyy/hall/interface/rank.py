# -*- coding: utf8 -*-



import time, json
import random
from lib.log import logger
from lib import sqlutil
from lib import userstruct

rankinfo = [0, []]

	
def handle(param):
	ranklistupdatetime, ranklist = rankinfo
	if time.time() - ranklistupdatetime > 60 * 5:
		rankinfo[0] = time.time()
		rankinfo[1] = sqlutil.execsql('SELECT userid, username, logo, exp FROM userinfo  ORDER BY exp DESC LIMIT 50')
		for r in rankinfo[1]:
			r['title'] = userstruct.getusertitle(r['exp'])


	return {'ret':1, 'data': json.dumps(rankinfo[1])}
		

