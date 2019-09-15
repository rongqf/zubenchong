
# -*- coding: utf8 -*-
import os,sys
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options
import tornado.log


import json
import time


from interface.lib.dbpool import dbpool
from interface.lib.RedisManager import rdsmanager
from interface.lib.log import logger




sqlcfg = {'host':"192.168.1.36",
    'user':'root',
    'passwd':'weakPasswdFWsfa989ewa',
    'db':'gamedb',
    'port':3306,
    'charset':'utf8'}

dbpool.initPool(**sqlcfg)



import interface.login
import interface.gamelist
import interface.getmap
import interface.getmapgen
import interface.collect

handdict = {'login': interface.login.handle,
			'gamelist': interface.gamelist.handle,
			'getmap': interface.getmap.handle,
			'getmapgen':interface.getmapgen.handle,
			'collect':interface.collect.handle,
			}



class ApiHandler(tornado.web.RequestHandler):
	def get(self):
		self.set_header("Access-Control-Allow-Origin", "*")
		self.set_header("Access-Control-Allow-Headers", "x-requested-with")
		self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')


		action = self.get_argument("action",None)
		var = self.get_argument("var",None)
		param = self.get_argument("param",None)

		logger.info('-' * 40 + '->')
		logger.info("%s:%s", action, param)

		if param:
			param = json.loads(param)
		if not action in handdict:
			ret = {'ret':1, 'desc':'action no found.'}
		else:
			rds = rdsmanager.get_client()

			t = time.time()
			ret = handdict[action](param)
			alltm = time.time() - t
			rkey = 'hashaction:%s' % action
			rds.hincrby(rkey, 'count', 1)
			logger.info("%s", alltm)
			rds.hincrbyfloat(rkey, 'time', alltm)
			#print rds.hgetall(rkey)
			
		self.write(json.dumps(ret))

		logger.info('<-' + '-' * 40)


class MainHandler(tornado.web.RequestHandler):
	def get(self):
		self.write('gamexxy')

class DebugInfo(tornado.web.RequestHandler):
	def get(self):

		rds = rdsmanager.get_client()
		tmp = rds.keys('hashaction:*')

		rst = {p:rds.hgetall(p) for p in tmp}

		self.write('%s' % rst)  
		
urlcfg = [(r"/", MainHandler),
		  (r"/debuginfo", DebugInfo),
		  (r"/api", ApiHandler),
		  ]


settings = {'debug' : True}
define("port", default=18888, help="run on the given port", type=int)
template_path = os.path.join(os.path.dirname(__file__), "template_path")
static_path = os.path.join(os.path.dirname(__file__), "static")

def main():
	
	tornado.options.parse_command_line()
	application = tornado.web.Application(
		urlcfg,
		**settings
		)
	http_server = tornado.httpserver.HTTPServer(application)
	http_server.listen(options.port)
	tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
	main()
