#coding:utf8

import json, time
from tornado import ioloop

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
	1:{'attackid': 1, 'attackname': u'断水', 'cost': 100,  'attacktime': 60 * 5, 'effectpoint': 2, 'effecttime': 0},
	2:{'attackid': 2, 'attackname': u'断网', 'cost': 120,  'attacktime': 60 * 5, 'effectpoint': 3, 'effecttime': 0},
	3:{'attackid': 3, 'attackname': u'断电', 'cost': 200,  'attacktime': 60 * 5, 'effectpoint': 4, 'effecttime': 0},
	4:{'attackid': 4, 'attackname': u'扔垃圾', 'cost': 150,  'attacktime': 60 * 5, 'effectpoint': 5, 'effecttime': 0},
}

def f2s():
	pass
ioloop.PeriodicCallback(f2s, 10000).start()


def getAttacPoint(aid):
	if aid in attackcfg:
		return attackcfg[aid]['cost']
	return 0


class AttackItem:
	def __init__(self):
		self.attackid = 0
		self.attacktime = 0

	def todict(self):
		d = {
		'attackid': self.attackid,
		'attacktime': self.attacktime,
		'endtime': self.attacktime
		}
		return d

	def updatedict(self, d):
		if d.get('attackid'): self.attackid = d.get('attackid')
		if d.get('attacktime'): self.attacktime = d.get('attacktime')

	def __repr__(self):
		return str([self.attackid, self.attacktime])

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

		self.map = [1, 1, 2, 2, 3, 4, 5, 0, 0, 0]
		self.buildlevel = [1, 1, 2, 2, 1, 1, 1, 0, 0, 0]
		self.attacks = [[] for _ in range(MapSize)]

	def __repr__(self):
		return str(self.__dict__)

	def getAttackDict(self):
		atmp = []
		for p in self.attacks:
			arr = []
			for q in p:
				arr.append(q.todict())
			atmp.append(arr)
		return atmp

	def todict(self):
		atmp = self.getAttackDict()

		d = {
			'map': self.map,
			'buildlevel': self.buildlevel,
			'updatetime': self.updatetime,
			'attacks': atmp,
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

	def getAttackNum(self, i, tm):
		ret = 0
		if 0 <= i < MapSize:
			b = self.map[i]
			l = self.buildlevel[i]
			u = self.updatetime[i]

			if b > 0 and l > 0:
				cfg = buildinglevelcfg[b][l]
				for p in self.attacks[i]:
					aendtm = p.attacktime + attackcfg[p.attackid]['attacktime']
					if aendtm > self.updatetime[i]:
						b = max(self.updatetime[i], p.attacktime)
						e = min(aendtm, tm)
						ret += int(e - b) * attackcfg[p.attackid]['effectpoint']
		return ret


	def addAttack(self, i, aid):
		if 0 <= i < MapSize:
			a = AttackItem()
			a.attackid = aid
			a.attacktime = time.time()

			self.attacks[i].append(a)
			return True
		return False

	def delAttack(self, i):
		ret = False
		if 0 <= i < MapSize:
			arr = []
			for p in self.attacks[i]:
				aid = p.attackid
				if p.attacktime + attackcfg[aid]['attacktime'] > time.time():
					arr.append(p)
			ret = len(arr) == len(self.attacks[i])
			self.attacks[i] = arr
		return ret

		
	def getGenAll(self):
		ret = [0 for _ in range(MapSize)]
		retflag = [False for _ in range(MapSize)]
		attackpoint = [0 for _ in range(MapSize)]
		buildstate = [1 for _ in range(MapSize)]
		for i in range(MapSize):
			b = self.map[i]
			l = self.buildlevel[i]
			u = self.updatetime[i]

			#self.delAttack(i)

			if b > 0 and l > 0:
				cfg = buildinglevelcfg[b][l]
				tmnow = time.time()
				t = tmnow - u
				if t > cfg['timeinterval'] + cfg['timedisabled']:
					ret[i] = 0
					retflag[i] = False
					buildstate[i] = 0
				elif t >= cfg['timeinterval']:
					attackpoint[i] = self.getAttackNum(i, u + cfg['timeinterval'])
					ret[i] = cfg['generate'] * cfg['timeinterval'] - attackpoint[i]
					ret[i] = max(0, ret[i])
					retflag[i] = True
				else:
					attackpoint[i] = self.getAttackNum(i, tmnow)
					ret[i] = int(t) * cfg['generate'] - attackpoint[i]
					ret[i] = max(0, ret[i])

		return {'gen':ret, 'genflag':retflag, 'attackpoint':attackpoint, 'buildstate': buildstate,
			'attacks':self.getAttackDict(),
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
			if u + cfg['timeinterval'] + cfg['timedisabled'] < time.time():
				self.updatetime[i] = time.time()
				return True
		return False


	def getGen(self, i):
		ret = 0
		retflag = False
		attackpoint  = 0
		buildstate = 1
		if 0 <= i < MapSize:
			b = self.map[i]
			l = self.buildlevel[i]
			u = self.updatetime[i]



			if b > 0 and l > 0:
				cfg = buildinglevelcfg[b][l]
				tmnow = time.time()
				t = tmnow - u
				if t > cfg['timeinterval'] + cfg['timedisabled']:
					ret = 0
					retflag = False
					buildstate = 0
				elif t >= cfg['timeinterval']:
					attackpoint = self.getAttackNum(i, tmnow)
					ret = cfg['generate'] * cfg['timeinterval'] - attackpoint
					ret = max(0, ret)
					retflag = True
				else:
					attackpoint = self.getAttackNum(i, tmnow)
					ret = int(t) * cfg['generate'] - attackpoint
					ret = max(0, ret)

		return {'gen':ret, 'genflag':retflag, 'attackpoint': attackpoint, 'buildstate': buildstate}

