#coding:utf8

import MJCard
import MJHuFun


class MJHandCard:

	def __init__(self):
		self.handcards = [
				[0], #fill size
				[0] * 10,#wan
				[0] * 10,#tiao
				[0] * 10,#bing
				[0] * 5,#feng
				[0] * 4,#jian
				[0] * 9,#hua
			]

		self.cardcut = 0
		self.laizi = None
	
	def addcard(self, c, p, cut = 1):
		cards = self.handcards
		cards[c][p] += cut
		self.cardcut += cut
		return cards

	def delcard(self, c, p, cut = 1):
		return self.addcard(c, p, -cut)

	def getcardnum(self, c, p):
		return self.handcards[c][p]

	def getlaizinum(self):
		if self.laizi:
			return self.getcardnum(self.laizi.getcolor(), self.laizi.getpoint())
		else:
			return 0

	def tocardlist(self):
		ret = []
		for i in range(1, len(self.handcards)):
			for j in range(1, len(self.handcards[i])):
				for k in range(self.handcards[i][j]):
					tmp = MJCard.MJCard(i, j)
					if self.laizi and tmp.getcolorpoint() == self.laizi.getcolorpoint():
						tmp.setislaizi()
					ret.append(tmp) 
		return ret


	def iscanchi(self, c, p):

		def _d(x):
			if x > 0:
				return 1
			else:
				return 0

		if not c in [MJCard.MJ_COLOR_WAN, MJCard.MJ_COLOR_TIAO, MJCard.MJ_COLOR_BING]:
			return False

		#ABX
		if 3 <= p:
			p1, p2 = p-1, p-2
			n1, n2 = _d(self.getcardnum(c, p1)), _d(self.getcardnum(c, p2))
			if n1 + n2 > 1:
				return True

		#AXB
		if 2 <= p <= 8:
			p1, p2 = p-1, p+1
			n1, n2 = _d(self.getcardnum(c, p1)), _d(self.getcardnum(c, p2))
			if n1 + n2 > 1:
				return True

		#XAB
		if p <= 7:
			p1, p2 = p+1, p+2
			n1, n2 = _d(self.getcardnum(c, p1)), _d(self.getcardnum(c, p2))
			if n1 + n2 > 1:
				return True

		return False

	def iscanchiex(self, ls):
		if len(ls) == 3:
			c = [x.getcolor() for x in ls]
			p = [x.getpoint() for x in ls]
			p.sort()
			if c[0] == c[1] == c[2] and 1 <= p[0] and p[2] <= 9 and p[0] == (p[1] - 1) == (p[2] - 2): 
				tmp = [(self.getcardnum(x.getcolor(), x.getpoint()) > 0) for x in ls]
				return tmp[1] == tmp[2] == True
			return False

	def iscanpeng(self, c, p):
		return self.getcardnum(c, p) >= 2

	def iscangang(self, c, p):
		return self.getcardnum(c, p) >= 3


	def prthu(self, hu):
		tmpfun = lambda x: ','.join(map(str, [MJCard.MJCard(p / 16, p % 16) for p in x]))
		for x in hu:
			print '|'.join(map(tmpfun, x)).decode('utf8')

	def iscanhuself(self):
		cardlist = self.tocardlist()
		tmp = [x.getint() for x in cardlist]
		ret = MJHuFun.huex(tmp)
		return ret
		
	def iscanhu(self, c, p):
		cardlist = self.tocardlist()
		tmp = [x.getint() for x in cardlist]
		tmp.append(MJCard.MJCard(c, p).getint())
		ret = MJHuFun.huex(tmp)
		return ret
		
	def iscanting(self):
		ret = []
		tmp = MJCard.MJGen().genunion()
		for x in tmp:
			if self.getcardnum(x.getcolor(), x.getpoint()) < 4:
				if self.iscanhu(x.getcolor(), x.getpoint()):
					ret.append([x.getcolor(), x.getpoint()])   
		return ret

	def tostr(self):
		cardlist = self.tocardlist()
		cardlist.sort()
		return 'laizi:%s' % self.laizi + '|' + ','.join(map(str, cardlist))


	def __str__(self):
		tmp = 'cut:%d\n' % self.cardcut
		if self.laizi:
			tmp = 'laizi:%s\n' % self.laizi
		tmp = tmp + '\n'.join([','.join(map(str, p)) for p in self.handcards])
		return tmp


if __name__ == '__main__':


	def prtl(ls):
		print 'prtl<<<<<<<<<<<<<<<<<'
		for x in ls:
			print str(x).decode('utf8')
		print 'prtl>>>>>>>>>>>>>>>>>'


	print '-----------------------------'
	#天衣无缝”九莲宝灯”
	tmp = [0x11, 0x11, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17, 0x18, 0x19, 0x19, 0x19]
	tc = [MJCard.MJCard(x / 16, x % 16) for x in tmp]
	prtl(tc)
	
	tc = sorted(tc)

	print 'aaaaaaaaaaaaaaaaaaaa'
	prtl(tc)

	ghc = MJHandCard()
	print ghc
	for x in tc:
		ghc.addcard(x.getcolor(), x.getpoint())
	
	print ghc

	print 'chi'

	print ghc.iscanchi(1, 1), 1, 1
	print ghc.iscanchi(1, 2), 1, 2
	print ghc.iscanchi(1, 3), 1, 3
	print ghc.iscanchi(1, 4), 1, 4
	print ghc.iscanchi(1, 5), 1, 5

	print '-------'
	print 'peng'
	print ghc.iscanpeng(1, 2), 1, 2
	print ghc.iscanpeng(1, 3), 1, 3

	print '--------'
	print 'hu'
	for x in range(1, 10):
		tmp = ghc.iscanhu(1, x)
		
		print len(tmp) > 0, 1, x
		ghc.prthu(tmp)

		
	print '--------'
	print 'ting'
	tmp = ghc.iscanting()
	tmp = [MJCard.MJCard(p[0], p[1]) for p in tmp]
	prtl(tmp)


	testtxt = '''
3334567888999
3334556677888
3334455667888
2344445678999
2333344567888
2223456777999
2223456777888
2223456777789
2223456677778
2223445566777
2223344556777
2223334567888
1233334567888
1113334567888
1112345666678
1112223456777
	'''

	def test(txt):
		h = MJHandCard()
		for x in txt:
			h.addcard(1, int(x))
		print h.tostr()
		tmp = h.iscanting()
		tmp = [MJCard.MJCard(p[0], p[1]) for p in tmp]
		print len(tmp)
		prtl(tmp)

	
	tmp = testtxt.split()
	for x in tmp:
		print '==================='
		test(x)
		

	print '--------------------------------------------------------'
	tmp = [0x21, 0x21, 0x21, 0x22, 0x22, 0x22, 0x14, 0x15, 0x16, 0x17, 0x29, 0x29, 0x29]
	tc = [MJCard.MJCard(x / 16, x % 16) for x in tmp]
	tc = sorted(tc)
	prtl(tc)
	ghc = MJHandCard()
	for x in tc:
		ghc.addcard(x.getcolor(), x.getpoint())
	ghc.laizi = MJCard.MJCard(1, 7)
	print ghc.tostr()
	print '--------'
	print 'hu'
	for x in range(1, 10):
		tmp = ghc.iscanhu(1, x)
		
		print len(tmp) > 0, 1, x
		ghc.prthu(tmp)
