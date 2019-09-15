#coding:utf8
import random
import time

import MJPlay
import MJCardPile
import MJCard

MJPLAYCUT = 4


CARD_ACTION_RUFFLE = 1
CARD_ACTION_DIZHUANG = 2
CARD_ACTION_DASAI = 3
CARD_ACTION_CHUPAI = 4

MJ_STATE_MOPAI = 1
MJ_STATE_CHUPAI = 2
MJ_STATE_ISCHI = 3
MJ_STATE_ISPENG = 4
MJ_STATE_ISGANG = 5
MJ_STATE_ISHU = 6
MJ_STATE_ISHUSELF = 7
MJ_STATE_GAMEOVER = 8

str_state = {
	MJ_STATE_MOPAI: '摸牌',
	MJ_STATE_CHUPAI: '出牌',
	MJ_STATE_ISCHI: '吃牌',
	MJ_STATE_ISPENG: '碰牌',
	MJ_STATE_ISGANG: '杠牌',
	MJ_STATE_ISHU: '胡牌',
	MJ_STATE_ISHUSELF: '自摸',
	MJ_STATE_GAMEOVER: '结束',
}

class CardAction:
	def __init__(self, atype, adata, tm):
		self.type = atype
		self.adata = adata
		self.time = tm



class Game:

	def __init__(self):
		self.palys = [MJPlay.MJPlayer() for _ in xrange(MJPLAYCUT)]
		self.ready = [False for _ in xrange(MJPLAYCUT)]

		self.cardpile = None

		self.zhuang = None
		self.laizi = None

		self.curplay = None
		self.state = None


		self.allaction = []


		self.cmd = open('cmd.txt').readlines()
		self.cmd = [s.replace('\n', '') for s in self.cmd]
		print self.cmd

		self.msg = ''

	def addaction(self, atype, adata):
		a = CardAction(atype, adata, time.clock())
		self.allaction.append(a)


	def nextplay(self):
		return (self.curplay + 1) % MJPLAYCUT

	def roundplay(self):
		return [(self.curplay + i + 1) % MJPLAYCUT for i in range(MJPLAYCUT - 1)]

	def card_ruffle(self):
		random.seed(1)
		self.cardpile = MJCardPile.MJCardPile()
		self.cardpile.ruffle()


		self.addaction(CARD_ACTION_RUFFLE, [1, self.cardpile.cards])


	def card_dizhuang(self):
		self.zhuang = random.randint(0, MJPLAYCUT - 1)

		self.addaction(CARD_ACTION_DIZHUANG, [self.zhuang])


	def card_dashai(self):

		x1, x2 = random.randint(1, 6), random.randint(1, 6)
		y1, y2 = random.randint(1, 6), random.randint(1, 6)

		p1 = (x1 + x2) % 4
		p2 = y1 + y2

		tmp = [26, 28, 26, 28]

		self.cardpile.setindexstart( sum(tmp[:p1]) + p2 )

		self.addaction(CARD_ACTION_DASAI, [p1, p2])

	def card_init(self):
		for i in xrange(MJPLAYCUT):
			c = self.cardpile.draw(13)
			for p in c:
				self.palys[i].mopai(p)

		self.addaction(CARD_ACTION_DASAI, [])


		self.curplay = self.zhuang

		p = self.cardpile.draw(1)
		self.palys[self.curplay].mopai(p[0])


		self.curplay = self.zhuang
		self.state = MJ_STATE_CHUPAI


	def checkbumo(self, card):
		action = [MJPlay.MJ_ACT_GANHU, MJPlay.MJ_ACT_GANGPAI, MJPlay.MJ_ACT_PENGPAI, MJPlay.MJ_ACT_CHIPAI]

		tmp = self.roundplay()
		for a in action:
			for p in tmp:
				if self.palys[p].iscanbumo(a, card):
					return [p, a]
		return None


	def onenterstate_MJ_STATE_MOPAI(self):
		p = self.cardpile.draw(1)
		self.palys[self.curplay].mopai(p[0])

		print 'mopai', str(p[0]).decode('utf8')
		print self.palys[self.curplay].handcard.tostr().decode('utf8')

		ret = self.palys[self.curplay].iscanhuself()
		if ret:
			self.curplay = self.curplay
			self.state = MJ_STATE_ISHUSELF

		else:
			self.curplay = self.curplay
			self.state = MJ_STATE_CHUPAI

		print '---------------------begin_onevnet_MJ_STATE_MOPAI'



	def onenterstate(self, state):

		eventcb = {MJ_STATE_MOPAI: self.onenterstate_MJ_STATE_MOPAI}
		if state in eventcb:
			print '---------------------begin_onenterstate_%s' % str_state[self.state].decode('utf8')
			print game.cardpile.prt().decode('utf8')
			for x in game.palys:
				print x.handcard.tostr().decode('utf8')

			eventcb[state]()

			print '++++++++++++++++++++++end_onenterstate_%s' % str_state[self.state].decode('utf8')
		


	def oninput(self):
		print str_state[self.state].decode('utf8'), self.curplay, self.zhuang

		if self.state == MJ_STATE_GAMEOVER:
			return False

		if len(self.cmd) > 0:
			msg = self.cmd[0]
			self.cmd = self.cmd[1:]
			print 'input:%s' % msg
			msg = msg.split(',')
		else:
			msg = raw_input('input:')
			msg = msg.split(',')


		if msg[0] == 'exit':
			self.curplay = self.curplay
			self.state = MJ_STATE_GAMEOVER

			return False
		else:
			if self.curplay == int(msg[0]):
				self.test(msg[1:])
		
		return True
		
	def test(self, msg):
		event = {
			MJ_STATE_CHUPAI : {'c': self.event_MJ_STATE_CHUPAI_c},

			MJ_STATE_ISCHI : {'c': self.event_MJ_STATE_ISCHI_c,
								'bc': self.event_MJ_STATE_ISCHI_bc
								},	
			MJ_STATE_ISPENG : {'p': self.event_MJ_STATE_ISPENG_p,
								'bp': self.event_MJ_STATE_ISPENG_bp
								},	
			MJ_STATE_ISGANG : {'g': self.event_MJ_STATE_ISGANG_g,
								'bg': self.event_MJ_STATE_ISGANG_bg
								},	
			MJ_STATE_ISHU : {'h': self.event_MJ_STATE_ISHU_h,
								'bh': self.event_MJ_STATE_ISHU_bh
								},	
			MJ_STATE_ISHUSELF : {'h': self.event_MJ_STATE_ISHUSELF_h,
								'bh': self.event_MJ_STATE_ISHUSELF_bh
								}			
		}
		if self.state in event:
			tmp = event[self.state]
			if msg[0] in tmp:
				self.msg = msg
				tmp[msg[0]]()
				self.onenterstate(self.state)


	def event_MJ_STATE_CHUPAI_c(self):

		msg = self.msg
		n = map(lambda x: int(x, 16), msg[1].split('|'))[0]
		cd = MJCard.MJCard.i2c(n)

		if self.palys[self.curplay].chupai(cd):

			self.addaction(CARD_ACTION_CHUPAI, [self.curplay, cd])

			bumo = self.checkbumo(cd)
			print 'check', bumo

			if bumo:
				p1, p2 = bumo

				tmp = {
					MJPlay.MJ_ACT_CHIPAI: MJ_STATE_ISCHI,
					MJPlay.MJ_ACT_PENGPAI: MJ_STATE_ISPENG,
					MJPlay.MJ_ACT_GANGPAI: MJ_STATE_ISGANG,
					MJPlay.MJ_ACT_GANHU: MJ_STATE_ISHU
					}

				self.curplay = p1
				self.state = tmp[p2]

			else:
				self.curplay = self.nextplay()
				self.state = MJ_STATE_MOPAI



	def event_MJ_STATE_ISCHI_c(self):
		msg = self.msg
		p = map(lambda x: int(x, 16), msg[1].split('|'))
		cd = [MJCard.MJCard.i2c(x) for x in p]

		print ','.join(map(str, cd)).decode('utf8')

		if self.palys[self.curplay].iscanchiex(cd):

			self.palys[self.curplay].chipai(cd)

			self.curplay = self.curplay
			self.state = MJ_STATE_CHUPAI


	def event_MJ_STATE_ISCHI_bc(self):
		pass

	def event_MJ_STATE_ISPENG_p(self):
		msg = self.msg
		n = map(lambda x: int(x, 16), msg[1].split('|'))[0]
		cd = MJCard.MJCard.i2c(n)

		if self.palys[self.curplay].iscanpeng(cd):

			self.palys[self.curplay].pengpai(cd)

			self.curplay = self.curplay
			self.state = MJ_STATE_CHUPAI

	def event_MJ_STATE_ISPENG_bp(self):
		pass

	def event_MJ_STATE_ISGANG_g(self):
		msg = self.msg
		n = map(lambda x: int(x, 16), msg[1].split('|'))[0]
		cd = MJCard.MJCard.i2c(n)

		if self.palys[self.curplay].iscangang(cd):

			self.palys[self.curplay].gangpai(cd)

			self.curplay = self.curplay
			self.state = MJ_STATE_CHUPAI

	def event_MJ_STATE_ISGANG_bg(self):
		pass

	def event_MJ_STATE_ISHU_h(self):
		msg = self.msg
		n = map(lambda x: int(x, 16), msg[1].split('|'))[0]
		cd = MJCard.MJCard.i2c(n)

		ret = self.palys[self.curplay].iscanhu(cd)
		if ret:
			self.curplay = self.curplay
			self.state = MJ_STATE_GAMEOVER
			print ret 

	def event_MJ_STATE_ISHU_bh(self):
		pass

	def event_MJ_STATE_ISHUSELF_h(self):
		msg = self.msg
		ret = self.palys[self.curplay].iscanhuself()
		if ret:
			self.curplay = self.curplay
			self.state = MJ_STATE_GAMEOVER
			print ret 

	def event_MJ_STATE_ISHUSELF_bh(self):
		pass


	def omtime(self, timeid):
		pass

	

if __name__ == '__main__':


	def prtl(ls):
		print 'prtl<<<<<<<<<<<<<<<<<'
		for x in ls:
			print str(x).decode('utf8')
		print 'prtl>>>>>>>>>>>>>>>>>'


	game = Game()
	game.card_ruffle()
	print game.cardpile.prt().decode('utf8')

	game.card_dizhuang()
	game.card_dashai()
	game.card_init()

	
	while game.oninput():
		pass

	print 'over'


