#coding:utf8

import json, time
from tornado import ioloop
import sqlutil

import logging
logger = logging.getLogger('hell')


MapSize = 20
MaxBuild = 20

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
guardcfg = {}

def ontimeReadDb():
	global attackcfg, buildinglevelcfg, guardcfg

	tmp = sqlutil.ReadDataFromDB('attackconfig')
	attackcfg = {}
	for p in tmp:
		attackcfg[p['attackid']] = p


	tmp = sqlutil.ReadDataFromDB('guardconfig')
	guardcfg = {}
	for p in tmp:
		guardcfg[p['guardid']] = p

	txt = json.dumps(attackcfg, encoding='utf-8', ensure_ascii=False, indent=2)
	#print(txt)
	logger.info(txt)

	bname = sqlutil.ReadDataFromDB('buildingconfig')
	name = {}
	for p in bname:
		name[p['buildid']] = p['name']


	logger.info(name)


	tmp = sqlutil.ReadDataFromDB('buildinglevelconfig')
	buildinglevelcfg = {}
	for p in tmp:
		buildinglevelcfg[p['buildid']] = {}
	for p in tmp:
		buildinglevelcfg[p['buildid']][p['level']] = p
	for p in buildinglevelcfg:
		buildinglevelcfg[p]['maxlevel'] = len(buildinglevelcfg[p]) - 1
		buildinglevelcfg[p]['name'] = name.get(p, '')

	txt = json.dumps(buildinglevelcfg, encoding='utf-8', ensure_ascii=False, indent=2)
	#print(txt)
	logger.info(txt)
	

ioloop.PeriodicCallback(ontimeReadDb, 1000 * 60 * 30).start()
ontimeReadDb()

def getAttacPoint(aid):
	if aid in attackcfg:
		return attackcfg[aid]['cost']
	return 0

def getGuardPoint(gid):
	if gid in guardcfg:
		return guardcfg[gid]['cost']
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

	def isValid(self):
		return time.time() <= self.begintime + self.attacktime

	def updatedict(self, d):
		if d.get('attackid'): self.attackid = d.get('attackid')
		if d.get('attacktime'): self.attacktime = d.get('attacktime')
		if d.get('begintime'): self.begintime = d.get('begintime')

	def guard(self, num):
		self.attacktime -= num
		self.attacktime = max(0, self.attacktime)

	def __repr__(self):
		return str([self.attackid, self.begintime, self.attacktime])

class EffectItem:
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

		self.map = [0 for _ in range(MapSize)]
		for i in range(5):
			self.map[i] = i + 1

		self.buildlevel = [0 for _ in range(MapSize)]
		self.attacks = [[] for _ in range(MapSize)]
		self.doubleinfo = [EffectItem() for _ in range(MapSize)]

		self.protectinfo = [EffectItem() for _ in range(MapSize)]

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
			'doubleinfo': [p.todict() for p in self.doubleinfo],
			'protectinfo': [p.todict() for p in self.protectinfo],
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

			if d.get('protectinfo'):
				dinfo = d.get('protectinfo')
				for i in range(len(dinfo)):
					self.protectinfo[i].updatedict(dinfo[i])

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
					b = max(self.updatetime[i], p.begintime)
					e = min(aendtm, tm)
					if b < e:
						ret += int(e - b) * attackcfg[p.attackid]['attackpoint']
		return ret


	def addAttack(self, i, aid):
		if 0 <= i < MapSize and aid in attackcfg:
			b = self.map[i]
			l = self.buildlevel[i]
			if b <= 0 and l <= 0:
				return False

			if self.protectinfo[i].valid():
				return False

			ishas = False
			self.delAttack(i)
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

	def guard(self, i, gid):
		if 0 <= i < MapSize and gid in guardcfg:
			self.delAttack(i)
			gcfg = guardcfg[gid]

			logger.debug("%s, %s", gcfg, self.attacks[i])

			if gcfg['guardtype'] == 1:
				for j, p in enumerate(self.attacks[i]):
					if p.attackid == gcfg['attackid']:
						self.attacks[i][j].guard(gcfg['guardtime'])
						return True

			elif gcfg['guardtype'] == 2:
				if len(self.attacks[i]) <= 0:
					if self.protectinfo[i].valid():
						self.protectinfo[i].validtime += gcfg['guardtime']
					else:
						self.protectinfo[i].begintime = time.time()
						self.protectinfo[i].validtime = gcfg['guardtime']
					return True

		return False



	def delAttack(self, i):
		ret = False
		if 0 <= i < MapSize:
			arr = []
			for p in self.attacks[i]:
				aid = p.attackid
				if p.isValid():
					arr.append(p)
			ret = len(arr) == len(self.attacks[i])
			self.attacks[i] = arr
		return ret

	def createBuild(self, i, bid):
		if self.map[i] == 0 and bid in buildinglevelcfg:
			self.map[i] = bid
			self.buildlevel[i] = 1
			self.buildstate[i] = 1
			self.updatetime[i] = time.time()
			return True
		return False


	def getSecAttack(self, i, tmnow):
		ret = 0
		if 0 <= i < MapSize:
			b = self.map[i]
			l = self.buildlevel[i]
			u = self.updatetime[i]

			if b > 0 and l > 0:
				cfg = buildinglevelcfg[b][l]
				for p in self.attacks[i]:
					aendtm = p.begintime + p.attacktime
					b = max(u, p.begintime)
					e = min(aendtm, tmnow)
					if b <= tmnow <= e:
						ret += attackcfg[p.attackid]['attackpoint']
		return ret

	def getSecDouble(self, i, tmnow):
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
						e = min(aendtm, tmnow)
						ret = cfg['generate']
		return ret
		
	def getGenAll(self):
		ret = [0 for _ in range(MapSize)]
		retflag = [False for _ in range(MapSize)]
		attackpoint = [0 for _ in range(MapSize)]

		gensec = 0

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
				elif t > cfg['timeinterval'] + cfg['timedisabled']:
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

					tmpsec = cfg['generate'] + self.getSecDouble(i, tmnow) - self.getSecAttack(i, tmnow)
					tmpsec = max(0, tmpsec)
					gensec += tmpsec

		return {'gen':ret, 'genflag':retflag, 'attackpoint':attackpoint, 'buildstate': self.buildstate,
			'updatetime': self.updatetime,
			'attacks':self.getAttackDict(), 
			'doubleinfo': [p.todict() for p in self.doubleinfo], 
			'protectinfo': [p.todict() for p in self.protectinfo], 
			'servertime': time.time(), 'gensec':gensec, 
		}

	def getUpgrade(self, i):
		if 0 <= i < MapSize:
			b = self.map[i]
			l = self.buildlevel[i]
			return buildinglevelcfg[b][l]['upgrade']
		return 0

	def getCreateBuild(self, bid, level):
		if bid in buildinglevelcfg:
			item = buildinglevelcfg[bid].get(level)
			if item:
				return item['upgrade']
		return 0


	def upgrade(self, i):
		if 0 <= i < MapSize:
			b = self.map[i]
			l = self.buildlevel[i]
			if l < buildinglevelcfg[b]['maxlevel']:
				self.buildlevel[i] += 1
				if self.buildstate[i] == 1:
					self.updatetime[i] = time.time()
				return True
		return False

	def getRecycle(self, i):
		if 0 <= i < MapSize:
			b = self.map[i]
			l = self.buildlevel[i]
			if b > 0 and l > 0:
				return buildinglevelcfg[b][l]['recycle']
		return 0

	def recycle(self, i):
		if 0 <= i < MapSize:
			self.buildlevel[i] = 0
			self.updatetime[i] = 0
			self.buildstate[i] = 1
			self.attacks[i] = []
			self.doubleinfo[i] = EffectItem()
			self.protectinfo[i] = EffectItem()
			return True
		return False

	def activate(self, i):
		
		if 0 <= i < MapSize:
			self.getGen(i)
			
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
				#logger.info("aaaaaaaaaaaaaa:%s", self.doubleinfo[i].valid())
				if self.doubleinfo[i].valid():
					self.doubleinfo[i].validtime += cfg['doubletime']
				else:
					self.doubleinfo[i].begintime = time.time()
					self.doubleinfo[i].validtime = cfg['doubletime']
				return True
		return False

	def getProtect(self, i):
		if 0 <= i < MapSize:
			b = self.map[i]
			l = self.buildlevel[i]
			if b > 0 and l > 0:
				self.delAttack(i)
				logger.info("aaaaaaaaaaaaaa:%s", self.attacks[i])
				if len(self.attacks[i]) <= 0:
					return buildinglevelcfg[b][l]['protectcost']
		return 0


	def protect(self, i):
		if 0 <= i < MapSize:
			b = self.map[i]
			l = self.buildlevel[i]
			if b > 0 and l > 0:
				cfg = buildinglevelcfg[b][l]
				#logger.info("aaaaaaaaaaaaaa:%s", self.doubleinfo[i].valid())
				if self.protectinfo[i].valid():
					self.protectinfo[i].validtime += cfg['protecttime']
				else:
					self.protectinfo[i].begintime = time.time()
					self.protectinfo[i].validtime = cfg['protecttime']
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
						if b < e:
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
			'updatetime': self.updatetime[i],
			'attacks':self.getAttackDict(i), 
			'doubleinfo': self.doubleinfo[i].todict(),
			'protectinfo': self.protectinfo[i].todict(),
			'servertime': time.time(),
		}

