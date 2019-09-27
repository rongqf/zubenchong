# -*- coding: utf8 -*-



import time, json
import random
from lib.log import logger
from lib import sqlutil
from lib import userstruct

from tornado import ioloop

marquee_loop = [0, []]
marquee_normal = []

def ontime():
	tm = int(time.time()) - 1

	for i in range(2):
		userstruct.pushmarquee('msgtest:%s, %s' % (tm + 1, 1))

	global marquee_normal
	marquee_normal = userstruct.getmarquee(tm)
	#print(tm+1, marquee_normal)

ioloop.PeriodicCallback(ontime, 1000).start()

def handle_loop(param):
	updatetime, marquee = marquee_loop
	if time.time() - updatetime > 60 * 5:
		marquee_loop[0] = time.time()
		marquee_loop[1] = sqlutil.execsql('select msg from marquee where valid = 1')
	return {'ret':1, 'data': marquee_loop[1]}
		

def handle_normal(param):
	global marquee_normal
	logger.debug(time.time())
	return {'ret':1, 'data': marquee_normal}

