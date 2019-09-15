#coding:utf8

import MJCard
import MJHandCard
import MJCardPile

MJPLAYCUT = 2
class Game:

	def __init__(self):
		self.palys = [MJPlayer() for x in range(MJPLAYCUT)]
		self.cardpile = MJCardPile()

		self.zhuang = None
		self.laizi = None

		self.curplay = None

		self.state = None


	def begin(self):
		pass

	def end(self):
		pass
