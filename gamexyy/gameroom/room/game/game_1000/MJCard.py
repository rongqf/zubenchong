#coding:utf8

MJ_NUM = ['零', '一', '二', '三', '四', '五', '六', '七', '八', '九']
MJ_WAN = [x + '万' for x in MJ_NUM]
MJ_TIAO = [x + '条' for x in MJ_NUM]
MJ_BING = [x + '饼' for x in MJ_NUM]
MJ_FENG = ['零', '东风', '南风', '西风', '北风']
MJ_JIAN = ['零', '中', '发', '白']
MJ_HUA= ['零', '春', '夏', '秋', '冬', '梅', '兰', '竹', '菊']
MJ_COLOR = ['零', '万', '条', '饼', '风', '箭', '花']
MJ_NAME = [[], MJ_WAN, MJ_TIAO, MJ_BING, MJ_FENG, MJ_JIAN, MJ_HUA]

MJ_COLOR_WAN = 1
MJ_COLOR_TIAO = 2
MJ_COLOR_BING = 3
MJ_COLOR_FENG = 4
MJ_COLOR_JIAN = 5
MJ_COLOR_HUA = 6


class MJCard:
	#int n = 00000|lai|color|point
	
	def __init__(self, color, point, index=-1):
		self.index = index
		self.card = color * 16 + point

	def setindex(self, index):
		self.index = index

	def setislaizi(self):
		self.card = 1 * (16 * 16) + self.card % (16 * 16)

	def getislaizi(self):
		return self.card // (16 * 16) % 16
	

	def getcolor(self):
		return self.card // 16 % 16

	def getpoint(self):
		return self.card % 16

	def getcolorpoint(self):
		return self.card % (16 * 16)
		
	def getintH(self):
		return '0x%x' % self.card
	
	def getint(self):
		return self.card

	def __cmp__(stc, dst):
		return stc.card % (16 * 16) - dst.card % (16 * 16)

	def __str__(self):
		v, c = self.getpoint(), self.getcolor()
		if 0 < c < len(MJ_NAME) and  0 < v < len(MJ_NAME[c]):
			return '%s' % (MJ_NAME[c][v]) 
		else:
			return 'i,c,v:%d,%d,%d' % (self.index, v, c)

	@classmethod
	def i2c(cls, x):
		ret = MJCard(x // 16 % 16, x % 16)
		if x // (16 * 16) % 16 > 0:
			ret.setislaizi()
		return ret



genwan = lambda:  [MJCard(MJ_COLOR_WAN, i) for i in range(1, 10)]
gentiao = lambda:  [MJCard(MJ_COLOR_TIAO, i) for i in range(1, 10)]
genbing = lambda: [MJCard(MJ_COLOR_BING, i) for i in range(1, 10)]
		
class MJGen:
	def gen(self):
		ret = genwan() + genwan() + genwan() + genwan() + \
			gentiao() + gentiao() + gentiao() + gentiao() + \
			genbing() + genbing() + genbing() + genbing()
		for i, x in enumerate(ret):
			x.setindex(i)
			
		return ret

	def genunion(self):
		return genwan() + gentiao() + genbing()



if __name__ == '__main__':
	#random.seed (1)
	print 0x1FF
	
	def test(n):
		print n>>8 & 0x0F,  n >> 4 & 0x0F, n & 0x0F
		print n // (16 * 16),  n // 16 % 16, n % 16
		print '%x' % n

	x = 0x1FF
	test(x)

	t = MJCard(MJ_COLOR_FENG, 5)
	print t
	t.setislaizi()
	print t.getintH()
	
	t = MJGen()
	t = t.gen()
	for p in t:
		print str(p).decode('utf8')
	
	print '----------------'
	c = MJCard.i2c(0x35)
	print 'aa', c
	print str(c).decode('utf8')
   
	#ghc.laizi = MJCard(
