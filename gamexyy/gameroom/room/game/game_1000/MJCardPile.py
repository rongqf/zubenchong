#coding:utf8

import random

import MJCard

class MJCardPile:
	def __init__(self):
		
		self.playcut = 4
		self.laizi = 0

		self.indexstart = -1
		self.indexcurrent = -1
		self.usecut = 0
	
		self.cards = MJCard.MJGen().gen()
		self.cardlen = len(self.cards)
		
		self.cardpos = [True for _ in xrange(self.cardlen)]

	def ruffle(self):
		random.shuffle(self.cards)
		return self.cards

	def setindexstart(self, index):
		self.indexstart = index
		self.indexcurrent = index

	def draw(self, count = 1):
		s = self.indexcurrent

		while not self.cardpos[s]:
			s += (s + 1) % self.cardlen
			if s == self.indexstart:
				return None

		t = (s + count) % self.cardlen
		self.indexcurrent = t
		self.usecut += count
		
		if s <= t:
			for i in range(s, t):
				self.cardpos[i] = False
			return self.cards[s:t]
		else:
			for i in list(range(s, self.cardlen)) + list(range(0, t)):
				self.cardpos[i] = False
			return self.cards[s:self.cardlen] + self.cards[0:t]


	def bugang(self):
		s = self.indexstart 
		s = (self.cardlen + s - 1) % self.cardlen
		while not self.cardpos[s]:
			s = (self.cardlen + s - 1) % self.cardlen
			if s == self.indexstart:
				return None
		self.cardpos[s] = False
		return self.cards[s]



	def __str__(self):
		return '%d,%d,%d' % (self.indexstart, self.indexcurrent, self.usecut)

	def tojson(self):
		cl = self.cardlen / 4
		return [self.cardpos[i*cl : (i+1) * cl] for i in range(4)]



	def prt(self):

		cardtxt = [str(self.cards[i]) if self.cardpos[i] else 'None' for i in xrange(self.cardlen)]

		tmp = zip(cardtxt[26:54], cardtxt[80:108][::-1])
		tmp = '\n'.join(map(lambda x: x[0] + ' '*130 + x[1], tmp)) + '\n'

		s1 = ','.join(cardtxt[0:26][::-1]) + '\n'
		s2 = ','.join(cardtxt[54:80]) + '\n'
		return ' '*4 + s1 + tmp + ' '*4 + s2



if __name__ == '__main__':

	def prtl(ls):
		print 'prtl<<<<<<<<<<<<<<<<<'
		for x in ls:
			print str(x).decode('utf8')
		print 'prtl>>>>>>>>>>>>>>>>>'
		
	t = MJCard.MJGen()
	t = t.gen()
	for p in t:
		pass
		#print str(p).decode('utf8')

	t = MJCardPile()
	random.seed(1)
	t.ruffle()
	t.setindexstart(105)

	print t.prt().decode('utf8')

	p = t.tojson()
	for x in p:
		print x

	for p in t.cards:
		pass
		#print str(p).decode('utf8')

	prtl(t.cards[104:t.cardlen] + t.cards[:10])
	prtl(t.draw())
	print t
	prtl(t.draw(4))
	print t
	prtl(t.draw(4))
	print t


	x = t.bugang()
	print x


	x = t.bugang()
	print x



	print t.prt().decode('utf8')
