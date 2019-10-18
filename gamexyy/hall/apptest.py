
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




sqlcfg = {'host':"127.0.0.1",
    'user':'root',
    'passwd':'112233',
    'db':'gamedb',
    'port':3306,
    'charset':'utf8'}

dbpool.initPool(**sqlcfg)



import interface.login
import interface.gamelist
import interface.getmap
import interface.getmapgen
import interface.collect
import interface.upgrade
import interface.userinfo
import interface.getcfg
import interface.activate
import interface.attack
import interface.userinfoother
import interface.rank
import interface.friend
import interface.marquee
import interface.changepwd
import interface.double
import interface.createBuild
import interface.register

handdict = {'login': interface.login.handle,
			'gamelist': interface.gamelist.handle,
			'getmap': interface.getmap.handle,
			'getmapgen':interface.getmapgen.handle,
			'collect':interface.collect.handle,
			'createBuild': interface.createBuild.handle,
			'upgrade':interface.upgrade.handle,
			'userinfo':interface.userinfo.handle,
			'getconfig':interface.getcfg.handle,
			'activate':interface.activate.handle,
			'attack':interface.attack.handle,
			'userinfoother':interface.userinfoother.handle,
			'rank':interface.rank.handle,

			'getfriend': interface.friend.handle_getfriend,
			'getfriendreq': interface.friend.handle_getfriendreq,
			'addfriend': interface.friend.handle_add,
			'acceptfriend': interface.friend.handle_accept,

			'getmarqueeloop': interface.marquee.handle_loop,
			'getmarqueenormal': interface.marquee.handle_normal,

			'changepwd': interface.changepwd.handle,

			'double': interface.double.handle,

			'register': interface.register.handle,
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

		if True:
		#try:
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
			
			logger.info(ret)	
			self.write(json.dumps(ret))
		#except Exception as e:
		#	logger.error(str(e))

		logger.info('<-' + '-' * 40)


class MainHandler(tornado.web.RequestHandler):
	def get(self):
		self.write('gamexxy')

class DebugInfo(tornado.web.RequestHandler):
	def get(self):

		txt = ''
		rds = rdsmanager.get_client()
		tmp = rds.keys('hashaction:*')
		rst = {}
		rst['hashaction'] = {p:rds.hgetall(p) for p in tmp}
		txt += json.dumps(rst['hashaction'], indent=2) + '<br><br>'

		tmp = rds.keys('hashuser:*')
		rst['hashuser'] = {p:rds.hgetall(p) for p in tmp}
		txt += json.dumps(rst['hashuser'], indent=2) + '<br><br>'

		tmp = rds.smembers('setupdateuser')
		rst['setupdateuser'] = list(tmp)
		txt += json.dumps(rst['setupdateuser'], indent=2) + '<br><br>'

		self.write(txt)  
		
urlcfg = [(r"/", MainHandler),
		  (r"/debuginfo", DebugInfo),
		  (r"/api", ApiHandler),
		  ]



define("port", default=18888, help="run on the given port", type=int)
template_path = os.path.join(os.path.dirname(__file__), "template_path")
static_path = os.path.join(os.path.dirname(__file__), "static")
settings = {'debug' : True}

def main():
	
	tornado.options.parse_command_line()
	application = tornado.web.Application(
		urlcfg,
        template_path = template_path,
        static_path = static_path,
		**settings
		)
	http_server = tornado.httpserver.HTTPServer(application)
	http_server.listen(options.port)
	tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
	main()
