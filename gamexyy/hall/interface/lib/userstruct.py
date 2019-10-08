#coding:utf8

import json, time, re

from RedisManager import rdsmanager
import sqlutil
import mapstruct
import logging
logger = logging.getLogger('hell')

import MySQLdb

usertitle = [
	{'exp': 1000, 'title': u'称号1'},
	{'exp': 4000, 'title': u'称号2'},
	{'exp': 10000, 'title': u'称号3'},
	{'exp': 20000, 'title': u'称号4'},
	{'exp': 50000, 'title': u'称号5'},
	{'exp': 80000, 'title': u'称号6'},
	{'exp': 100000, 'title': u'称号7'},
	{'exp': 500000, 'title': u'称号8'},
]

def getusertitle(exp):
	if exp < usertitle[0]['exp']:
		#return ''
		return 0
	if exp >= usertitle[-1]['exp']:
		#return usertitle[-1]['title']
		return len(usertitle)
	for i in range(1, len(usertitle)):
		if exp < usertitle[i]['exp']:
			#return usertitle[i - 1]['title']
			return i + 1


class UserStruct(object):
	"""docstring for MapInfo"""
	def __init__(self):
		self.userid = 0
		self.password = ''
		self.gamepoint = 0
		self.money = 0
		self.exp = 0
		self.logo = 1
		self.username = ''
		self.skey = ''
		self.update_time = 0
		self.mapstr = ''
		self.mapdata = None

	def __repr__(self):
		return str(self.__dict__)

	def tomap(self):
		d = {
			'userid': self.userid,
			'password': self.password,
			'gamepoint': self.gamepoint,
			'money': self.money,
			'exp': self.exp,
			'logo': self.logo,
			'username': self.username,
			'skey': self.skey,
			'update_time':self.update_time,
		}
		return d

	def todict(self):
		d = {
			'userid': self.userid,
			'gamepoint': self.gamepoint,
			'exp': self.exp,
			'logo': self.logo,
			'username': self.username,
			'skey': self.skey,
			'exp': self.exp,
			'title': getusertitle(self.exp),
		}
		return d

	def tojson(self):
		d = self.todict()
		return json.dumps(d)

	def update(self, d):
		#logger.debug(d)
		if isinstance(d, dict):
			if d.get('userid'): self.userid = int(d.get('userid'))
			if d.get('password'): self.password = d.get('password')
			if d.get('gamepoint'): self.gamepoint = int(d.get('gamepoint'))
			if d.get('money'): self.money = int(d.get('money'))
			if d.get('exp'): self.exp = int(d.get('exp'))
			if d.get('logo'): self.logo = int(d.get('logo'))
			if d.get('username'): self.username = d.get('username')
			if d.get('skey'): self.skey = d.get('skey')
			if d.get('update_time'): self.update_time = float(d.get('update_time'))
			if d.get('mapdata'): self.mapstr = d.get('mapdata')

			#logger.debug(self)

	def update_point(self, point):
		pass

	def update_money(self, money):
		pass


	def getmap(self):
		if not self.mapdata and self.mapstr != '':
			mapdata = mapstruct.MapInfo()
			mapdata.updatejson(self.mapstr)
			self.mapdata = mapdata
		return self.mapdata


def read_mysql(username):
	username = MySQLdb.escape_string(username)
	tmp = sqlutil.GetOneRecordInfo('userinfo', {'username':username})
	if tmp:
		u = UserStruct()
		u.update(tmp)
		return u
	return None

def read_mysql_userid(uid):
	tmp = sqlutil.GetOneRecordInfo('userinfo', {'id':uid})
	if tmp:
		u = UserStruct()
		u.update(tmp)
		return u
	return None




def read_redis(userid, filed = None):
	rds = rdsmanager.get_client(userid)
	rkey = 'hashuser:%s' % userid
	if not filed:
		userinfo = rds.hgetall(rkey)
		if userinfo:
			u = UserStruct()
			u.update(userinfo)
			return u
	else:
		return rds.hmget(filed)
	return None



def write_redis_dict(useid, d):
	d.update({'update_time': time.time()})
	rds = rdsmanager.get_client(useid)
	rkey = 'hashuser:%s' % useid
	rds.hmset(rkey, d)

def write_redis_all(user):
	d = user.tomap()
	write_redis_dict(user.userid, d)


def write_redis_updateuser(useid):
	rds = rdsmanager.get_client()
	rkey = 'setupdateuser'
	rds.sadd(rkey, useid) 



def read_user(userid):
	user = read_redis(userid)
	if not user:
		user = read_mysql_userid(userid)
		if user:
			write_redis_all(user)
	return user


def pushmarquee(msg):
	rds = rdsmanager.get_client()
	tm = int(time.time())
	rkey = 'marquee:%s' % tm
	rds.rpush(rkey, msg)
	rds.expireat(rkey, tm + 60)

def getmarquee(tm):
	rds = rdsmanager.get_client()
	rkey = 'marquee:%s' % tm
	l = rds.llen(rkey)
	return rds.lrange(rkey, 0, l)




def checkpwdfrt(pwd):
	if len(pwd) < 6:
		return False

	return True





if __name__ == '__main__':

	print getmarquee(1569559605)

	print checkpwdfrt('123456*&_,中w')
