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


	def clear(self):
		self.palys = [MJPlay.MJPlayer() for _ in xrange(MJPLAYCUT)]
		self.ready = [False for _ in xrange(MJPLAYCUT)]

		self.cardpile = None

		self.zhuang = None
		self.laizi = None

		self.curplay = None
		self.state = None


		self.allaction = []


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

		self.state = MJ_STATE_CHUPAI


	def checkbumo(self, card):
		action = [MJPlay.MJ_ACT_GANHU, MJPlay.MJ_ACT_GANGPAI, MJPlay.MJ_ACT_PENGPAI, MJPlay.MJ_ACT_CHIPAI]

		tmp = self.roundplay()
		for a in action:
			for p in tmp:
				if self.palys[p].iscanbumo(a, card):
					return [p, a]
		return None

	def dostatechange(self):

		print game.cardpile.prt().decode('utf8')
		for x in game.palys:
			print x.handcard.tostr().decode('utf8')

		if self.state == MJ_STATE_MOPAI:
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


	def ongamemsg(self, index, msg):

		print str_state[self.state].decode('utf8'), self.curplay, self.zhuang

		if msg[0] == 'exit':
			self.curplay = self.curplay
			self.state = MJ_STATE_GAMEOVER

		if self.state == MJ_STATE_CHUPAI:
			if index == self.curplay and msg[0] == 'c':
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
			else:
				print 'error input'
				self.oninput()


		if self.state == MJ_STATE_ISCHI:
			if index == self.curplay and msg[0] == 'c':
				p = map(lambda x: int(x, 16), msg[1].split('|'))
				cd = [MJCard.MJCard.i2c(x) for x in p]

				print ','.join(map(str, cd)).decode('utf8')

				if self.palys[self.curplay].iscanchiex(cd):

					self.palys[self.curplay].chipai(cd)

					self.curplay = self.curplay
					self.state = MJ_STATE_CHUPAI


		if self.state == MJ_STATE_ISPENG:
			if index == self.curplay and msg[0] == 'p':
				n = map(lambda x: int(x, 16), msg[1].split('|'))[0]
				cd = MJCard.MJCard.i2c(n)

				if self.palys[self.curplay].iscanpeng(cd):

					self.palys[self.curplay].pengpai(cd)

					self.curplay = self.curplay
					self.state = MJ_STATE_CHUPAI

		if self.state == MJ_STATE_ISGANG:
			if index == self.curplay and msg[0] == 'g':
				n = map(lambda x: int(x, 16), msg[1].split('|'))[0]
				cd = MJCard.MJCard.i2c(n)

				if self.palys[self.curplay].iscangang(cd):

					self.palys[self.curplay].gangpai(cd)

					self.curplay = self.curplay
					self.state = MJ_STATE_CHUPAI

		if self.state == MJ_STATE_ISHU:
			if index == self.curplay and msg[0] == 'h':
				n = map(lambda x: int(x, 16), msg[1].split('|'))[0]
				cd = MJCard.MJCard.i2c(n)

				ret = self.palys[self.curplay].iscanhu(cd)
				if ret:
					self.curplay = self.curplay
					self.state = MJ_STATE_GAMEOVER
					print ret 

		if self.state == MJ_STATE_ISHUSELF:
			if index == self.curplay and msg[0] == 'h':
				ret = self.palys[self.curplay].iscanhuself()
				if ret:
					self.curplay = self.curplay
					self.state = MJ_STATE_GAMEOVER
					print ret 

		self.dostatechange()

	def omtime(self, timeid):
		pass

	def isgameover(self):
		return self.state == MJ_STATE_GAMEOVER
	

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


	cmd = open('cmd.txt').readlines()
	cmd = [s.replace('\n', '') for s in cmd]
	print cmd

	def getmsg():
		global cmd
		if len(cmd) > 0:
			msg = cmd[0]
			cmd = cmd[1:]
			print 'input:%s' % msg
			msg = msg.split(',')
		else:
			msg = raw_input('input:')
			msg = msg.split(',')
		return msg

	while not game.isgameover():
		msg = getmsg()
		game.ongamemsg(int(msg[0]), msg[1:])

	print 'game over!!!'


