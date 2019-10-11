#coding:utf8

import json, time
from tornado import ioloop
import sqlutil

import logging
logger = logging.getLogger('hell')


MapSize = 10
buildinglevelcfg = {
	1: {
		0: {'timeinterval': 0, 'generate': 0, 'upgrade': 100, 'timedisabled': 600},
		1: {'timeinterval': 15, 'generate': 10, 'upgrade': 100, 'timedisabled': 600},
		2: {'timeinterval': 15, 'generate': 20, 'upgrade': 200, 'timedisabled': 600},
		3: {'timeinterval': 15, 'generate': 30, 'upgrade': 300, 'timedisabled': 600},
		4: {'timeinterval': 15, 'generate': 40, 'upgrade': 400, 'timedisabled': 600}, 
		5: {'timeinterval': 15, 'generate': 50, 'upgrade': 400, 'timedisabled': 600}, 
		'maxlevel': 5,
	},
	2: {
		0: {'timeinterval': 0, 'generate': 0, 'upgrade': 100, 'timedisabled': 600},
		1: {'timeinterval': 15, 'generate': 10, 'upgrade': 100, 'timedisabled': 600},
		2: {'timeinterval': 15, 'generate': 20, 'upgrade': 200, 'timedisabled': 600},
		3: {'timeinterval': 15, 'generate': 30, 'upgrade': 300, 'timedisabled': 600},
		4: {'timeinterval': 15, 'generate': 40, 'upgrade': 400, 'timedisabled': 600}, 
		5: {'timeinterval': 15, 'generate': 50, 'upgrade': 500, 'timedisabled': 600}, 
		'maxlevel': 5,
	},
	3: {
		0: {'timeinterval': 0, 'generate': 0, 'upgrade': 100, 'timedisabled': 600},
		1: {'timeinterval': 10, 'generate': 11, 'upgrade': 500, 'timedisabled': 600},
		2: {'timeinterval': 10, 'generate': 22, 'upgrade': 600, 'timedisabled': 600},
		3: {'timeinterval': 10, 'generate': 33, 'upgrade': 70, 'timedisabled': 600},
		4: {'timeinterval': 10, 'generate': 44, 'upgrade': 800, 'timedisabled': 600}, 
		5: {'timeinterval': 15, 'generate': 50, 'upgrade': 900, 'timedisabled': 600}, 
		'maxlevel': 5,
	},
	4: {
		0: {'timeinterval': 0, 'generate': 0, 'upgrade': 100, 'timedisabled': 600},
		1: {'timeinterval': 10, 'generate': 11, 'upgrade': 500, 'timedisabled': 600},
		2: {'timeinterval': 10, 'generate': 22, 'upgrade': 600, 'timedisabled': 600},
		3: {'timeinterval': 10, 'generate': 33, 'upgrade': 700, 'timedisabled': 600},
		4: {'timeinterval': 10, 'generate': 44, 'upgrade': 800, 'timedisabled': 600}, 
		5: {'timeinterval': 15, 'generate': 50, 'upgrade': 900, 'timedisabled': 600}, 
		'maxlevel': 5,
	},
	5: {
		0: {'timeinterval': 0, 'generate': 0, 'upgrade': 100, 'timedisabled': 600},
		1: {'timeinterval': 8, 'generate': 13, 'upgrade': 600, 'timedisabled': 600},
		2: {'timeinterval': 8, 'generate': 24, 'upgrade': 700, 'timedisabled': 600},
		3: {'timeinterval': 8, 'generate': 35, 'upgrade': 800, 'timedisabled': 600},
		4: {'timeinterval': 8, 'generate': 46, 'upgrade': 900, 'timedisabled': 600}, 
		5: {'timeinterval': 8, 'generate': 50, 'upgrade': 1000, 'timedisabled': 600}, 
		'maxlevel': 5,
	},
}



attackcfg = {
	1:{'attackid': 1, 'attackname': u'断水', 'cost': 100,  'attacktime': 60 * 5, 'attackpoint': 2,},
	2:{'attackid': 2, 'attackname': u'断网', 'cost': 120,  'attacktime': 60 * 5, 'attackpoint': 3,},
	3:{'attackid': 3, 'attackname': u'断电', 'cost': 200,  'attacktime': 60 * 5, 'attackpoint': 4,},
	4:{'attackid': 4, 'attackname': u'扔垃圾', 'cost': 150,  'attacktime': 60 * 5, 'attackpoint': 5,},
}

def ontimeReadDb():
	global attackcfg, buildinglevelcfg

	tmp = sqlutil.ReadDataFromDB('attackconfig')
	attackcfg = {}
	for p in tmp:
		attackcfg[p['attackid']] = p

	txt = json.dumps(attackcfg, encoding='utf-8', ensure_ascii=False, indent=2)
	print(txt)
	logger.info(txt)

	tmp = sqlutil.ReadDataFromDB('buildinglevelconfig')
	buildinglevelcfg = {}
	for p in tmp:
		buildinglevelcfg[p['buildid']] = {}
	for p in tmp:
		buildinglevelcfg[p['buildid']][p['level']] = p
	for p in buildinglevelcfg:
		buildinglevelcfg[p]['maxlevel'] = len(buildinglevelcfg[p]) - 1

	txt = json.dumps(buildinglevelcfg, encoding='utf-8', ensure_ascii=False, indent=2)
	print(txt)
	logger.info(txt)
	

ioloop.PeriodicCallback(ontimeReadDb, 1000 * 60 * 30).start()
ontimeReadDb()

def getAttacPoint(aid):
	if aid in attackcfg:
		return attackcfg[aid]['cost']
	return 0


class AttackItem:
	def __init__(self):
		self.attackid = 0
		self.begintime = 0
		self.attacktime = 0

	def todict(self):
		d = {
		'attackid': self.attackid,
		'attacktime': self.attacktime,
		'begintime': self.begintime
		}
		return d

	def updatedict(self, d):
		if d.get('attackid'): self.attackid = d.get('attackid')
		if d.get('attacktime'): self.attacktime = d.get('attacktime')
		if d.get('begintime'): self.begintime = d.get('begintime')

	def __repr__(self):
		return str([self.attackid, self.begintime, self.attacktime])

class DoubleItem:
	def __init__(self):
		self.begintime = 0
		self.validtime = 0

	def valid(self):
		return self.begintime + self.validtime > time.time()

	def todict(self):
		d = {
		'validtime': self.validtime,
		'begintime': self.begintime,
		'valid': self.valid(),
		}
		return d

	def updatedict(self, d):
		if d.get('begintime'): self.begintime = d.get('begintime')
		if d.get('validtime'): self.validtime = d.get('validtime')

	def __repr__(self):
		return str([self.validtime, self.begintime])


class Builder:
	def __init__(self):
		self.bid = 0
		self.level = 0
		self.state = 1
		self.updatetime = 0
		self.attacks = []
		

	def todict(self):
		atmp = []
		for p in self.attacks:
			arr = []
			for q in p:
				arr.append(q)
			atmp.append(arr)

		d = {
			'bid': self.bid,
			'level': self.level,
			'state': self.state,
			'updatetime': self.updatetime,
			'attacks': atmp,
		}
		return d

	def updatedict(self, d):
		if d.get('bid'): self.bid = d.get('bid')
		if d.get('level'): self.level = d.get('level')
		if d.get('state'): self.updatetime = d.get('state')
		if d.get('updatetime'): self.buildstate = d.get('updatetime')
		if d.get('attacks'):
			self.attacks = []
			for p in d.get('attacks'):
				a = AttackItem()
				a.updatedict(p)
				self.attacks.append(a)


	def getGen(self):
		ret = 0
		retflag = False

		b = self.bid
		l = self.level
		u = self.updatetime
		if b > 0 and l > 0:
			cfg = buildinglevelcfg[b][l]
			t = time.time() - u
			if t > cfg['timeinterval'] + cfg['timedisabled']:
				self.state = 0
			elif t >= cfg['timeinterval']:
				ret = cfg['generate']
				retflag = True
			else:
				ret = int(t / cfg['timeinterval'] * cfg['generate'])

		return {'gen':ret, 'genflag':retflag, 'buildstate': self.state}




class MapInfo(object):
	"""docstring for MapInfo"""
	def __init__(self):
		self.map = [0 for _ in range(MapSize)]
		self.buildlevel = [0 for _ in range(MapSize)]
		self.updatetime = [time.time() for _ in range(MapSize)]
		self.buildstate = [1 for _ in range(MapSize)]

		self.map = [1, 1, 2, 2, 3, 4, 5, 0, 0, 0]
		self.buildlevel = [1, 1, 2, 2, 1, 1, 1, 0, 0, 0]
		self.attacks = [[] for _ in range(MapSize)]
		self.doubleinfo = [DoubleItem() for _ in range(MapSize)]

	def __repr__(self):
		return str(self.__dict__)

	def getAttackDict(self, index = -1):
		if index == -1:
			atmp = []
			for p in self.attacks:
				arr = []
				for q in p:
					arr.append(q.todict())
				atmp.append(arr)
			return atmp
		else:
			arr = []
			for q in self.attacks[index]:
				arr.append(q.todict())
			return arr

	def todict(self):
		atmp = self.getAttackDict()

		d = {
			'map': self.map,
			'buildlevel': self.buildlevel,
			'updatetime': self.updatetime,
			'buildstate': self.buildstate,
			'attacks': atmp,
			'doubleinfo': [p.todict() for p in self.doubleinfo]
		}
		return d

	def tojson(self):
		return json.dumps(self.todict())

	def updatejson(self, d):
		#logger.debug("updatejson: %s", d)
		if d != '':
			d = json.loads(d)
			if d.get('map'): self.map = d.get('map')
			if d.get('buildlevel'): self.buildlevel = d.get('buildlevel')
			if d.get('updatetime'): self.updatetime = d.get('updatetime')
			if d.get('buildstate'): self.buildstate = d.get('buildstate')
			if d.get('attacks'):
				self.attacks = []
				for p in d.get('attacks'):
					arr = []
					for q in p:
						#logger.debug("item: %s", q)
						a = AttackItem()
						a.updatedict(q)
						arr.append(a)
					self.attacks.append(arr)
				for i in range(MapSize):
					self.delAttack(i)

			if d.get('doubleinfo'):
				dinfo = d.get('doubleinfo')
				for i in range(len(dinfo)):
					self.doubleinfo[i].updatedict(dinfo[i])


	def getAttackNum(self, i, tm):
		ret = 0
		if 0 <= i < MapSize:
			b = self.map[i]
			l = self.buildlevel[i]
			u = self.updatetime[i]

			if b > 0 and l > 0:
				cfg = buildinglevelcfg[b][l]
				for p in self.attacks[i]:
					aendtm = p.begintime + p.attacktime
					if aendtm > self.updatetime[i]:
						b = max(self.updatetime[i], p.begintime)
						e = min(aendtm, tm)
						ret += int(e - b) * attackcfg[p.attackid]['attackpoint']
		return ret


	def addAttack(self, i, aid):
		if 0 <= i < MapSize:
			ishas = False
			for j in range(len(self.attacks[i])):
				if self.attacks[i][j].attackid == aid:
					self.attacks[i][j].attacktime += attackcfg[aid]['attacktime']
					ishas = True
					break
			if not ishas:
				a = AttackItem()
				a.attackid = aid
				a.begintime = time.time()
				a.attacktime = attackcfg[aid]['attacktime']
				self.attacks[i].append(a)
			return True
		return False


	def delAttack(self, i):
		ret = False
		if 0 <= i < MapSize:
			arr = []
			for p in self.attacks[i]:
				aid = p.attackid
				if p.begintime + p.attacktime > time.time():
					arr.append(p)
			ret = len(arr) == len(self.attacks[i])
			self.attacks[i] = arr
		return ret

		
	def getGenAll(self):
		ret = [0 for _ in range(MapSize)]
		retflag = [False for _ in range(MapSize)]
		attackpoint = [0 for _ in range(MapSize)]
		for i in range(MapSize):
			b = self.map[i]
			l = self.buildlevel[i]
			u = self.updatetime[i]

			#self.delAttack(i)

			if b > 0 and l > 0:
				cfg = buildinglevelcfg[b][l]
				tmnow = time.time()
				t = tmnow - u
				if self.buildstate[i] == 0:
					pass
				if t > cfg['timeinterval'] + cfg['timedisabled']:
					if self.buildstate[i] != 0:
						self.buildstate[i] = 2
						attackpoint[i] = self.getAttackNum(i, u + cfg['timeinterval'])
						ret[i] = cfg['generate'] * cfg['timeinterval'] - attackpoint[i] + self.getDoubleNum(i, u + cfg['timeinterval'])
						ret[i] = max(0, ret[i])
						retflag[i] = True
				elif t >= cfg['timeinterval']:
					attackpoint[i] = self.getAttackNum(i, u + cfg['timeinterval'])  
					ret[i] = cfg['generate'] * cfg['timeinterval'] - attackpoint[i] + self.getDoubleNum(i, u + cfg['timeinterval'])
					ret[i] = max(0, ret[i])
					retflag[i] = True
				else:
					attackpoint[i] = self.getAttackNum(i, tmnow)
					ret[i] = int(t) * cfg['generate'] - attackpoint[i]  + self.getDoubleNum(i, tmnow)
					ret[i] = max(0, ret[i])

		return {'gen':ret, 'genflag':retflag, 'attackpoint':attackpoint, 'buildstate': self.buildstate,
			'attacks':self.getAttackDict(), 'doubleinfo': [p.todict() for p in self.doubleinfo]
		}

	def getUpgrade(self, i):
		if 0 <= i < MapSize:
			b = self.map[i]
			l = self.buildlevel[i]
			return buildinglevelcfg[b][l]['upgrade']
		return 0

	def upgrade(self, i):
		if 0 <= i < MapSize:
			b = self.map[i]
			l = self.buildlevel[i]
			if l < buildinglevelcfg[b]['maxlevel']:
				self.buildlevel[i] += 1
				return True
		return False

	def activate(self, i):
		if 0 <= i < MapSize:
			b = self.map[i]
			l = self.buildlevel[i]
			u = self.updatetime[i]
			cfg = buildinglevelcfg[b][l]
			#if u + cfg['timeinterval'] + cfg['timedisabled'] < time.time():
			#	self.updatetime[i] = time.time()
			if self.buildstate[i] == 0:
				self.buildstate[i] = 1
				self.updatetime[i] = time.time()
				return True
			elif self.buildstate[i] == 2:
				self.buildstate[i] = 1
				return True
				
		return False

	def getDouble(self, i):
		if 0 <= i < MapSize:
			b = self.map[i]
			l = self.buildlevel[i]
			if b > 0 and l > 0:
				return buildinglevelcfg[b][l]['doublecost']
		return 0

	def double(self, i):
		if 0 <= i < MapSize:
			b = self.map[i]
			l = self.buildlevel[i]
			if b > 0 and l > 0:
				cfg = buildinglevelcfg[b][l]
				logger.info("aaaaaaaaaaaaaa:%s", self.doubleinfo[i].valid())
				if self.doubleinfo[i].valid():
					self.doubleinfo[i].validtime += cfg['doubletime']
				else:
					self.doubleinfo[i].begintime = time.time()
					self.doubleinfo[i].validtime = cfg['doubletime']
				return True
		return False


	def getDoubleNum(self, i, tm):
		ret = 0
		if 0 <= i < MapSize:
			b = self.map[i]
			l = self.buildlevel[i]
			u = self.updatetime[i]
			if b > 0 and l > 0:
				cfg = buildinglevelcfg[b][l]
				p = self.doubleinfo[i]
				if p.valid():
					aendtm = p.begintime + p.validtime
					if aendtm > self.updatetime[i]:
						b = max(self.updatetime[i], p.begintime)
						e = min(aendtm, tm)
						ret = int(e - b) * cfg['generate']
		return ret

	def getGen(self, i):
		ret = 0
		retflag = False
		attackpoint  = 0
		if 0 <= i < MapSize:
			b = self.map[i]
			l = self.buildlevel[i]
			u = self.updatetime[i]

			if b > 0 and l > 0:
				cfg = buildinglevelcfg[b][l]
				tmnow = time.time()
				t = tmnow - u

				if self.buildstate[i] == 0:
					pass
				elif t > cfg['timeinterval'] + cfg['timedisabled']:
					if self.buildstate[i] != 0:
						attackpoint = self.getAttackNum(i, u + cfg['timeinterval'])
						ret = cfg['generate'] * cfg['timeinterval'] - attackpoint + self.getDoubleNum(i, u + cfg['timeinterval'])
						ret = max(0, ret)
						retflag = True
						self.buildstate[i] = 2
				elif t >= cfg['timeinterval']:
					attackpoint = self.getAttackNum(i, u + cfg['timeinterval'])
					ret = cfg['generate'] * cfg['timeinterval'] - attackpoint + self.getDoubleNum(i, u + cfg['timeinterval'])
					ret = max(0, ret)
					retflag = True
				else:
					attackpoint = self.getAttackNum(i, tmnow)
					ret = int(t) * cfg['generate'] - attackpoint + self.getDoubleNum(i, tmnow)
					ret = max(0, ret)

		return {'gen':ret, 'genflag':retflag, 'attackpoint': attackpoint, 'buildstate': self.buildstate[i],
			'attacks':self.getAttackDict(i), 'doubleinfo': self.doubleinfo[i].todict(),
		}

