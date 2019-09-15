#coding:utf8

cut = 0

def hu(keys, clen, jingp, ls):
	global cut
	cut += 1
	
	if clen == 0:
		return [[]]
	if clen == 3 and ls[jingp] == 3:
		return  [[[jingp] * 3]]
	if clen >= 3:
		s0 = None
		for x in keys:
			if x != jingp and ls[x] > 0:
				s0 = x
				break
		sj, s1, s2 = jingp, s0 - 1, s0 - 2

		tmp = []
		if ls[s0] >= 3:
			tmp.append([s0, s0, s0])
		if ls[s1] > 0  and ls[s2] > 0:
			tmp.append([s0, s1, s2])
		#有赖子
		if ls[sj] > 0: 
			if ls[s0] > 1:
				tmp.append([sj, s0, s0])
			if ls[s1] > 0:
				tmp.append([sj, s0, s1])
			if ls[s2] > 0:
				tmp.append([sj, s0, s2])
			if ls[sj] > 1:
				tmp.append([sj, sj, s0])

		rst = [[]]
		for it in tmp:
			for p in it:
				ls[p] -= 1

			ttt =  hu(keys, clen - 3, jingp, ls)
			rst.append(map(lambda x: [it] + x, ttt))
			for p in it:
				ls[p] += 1

		return reduce(lambda x, y: x + y, rst)


from collections import Counter

def huex(ls):
	global cut
	cut = 0
	rst = []
	cardlen = len(ls)
	if cardlen % 3 == 2:
		ls.sort(key=lambda x: -x)
		jiang = []
		tmpset = set()
		for i in xrange(cardlen - 1):
			for j in xrange(i+1, cardlen):
				if ls[i] == ls[j] or ls[i] + ls[j] >= 250:
					if ls[i] * 250 + ls[j] not in tmpset:
						jiang.append([ls[i], ls[j]])
						tmpset.add(ls[i] * 250 + ls[j])

		tmp = Counter(ls)
		keys = tmp.keys()
		keys.sort(key=lambda x: -x)
		if keys[0] >= 250:
			jingp = keys[0]
		else:
			jingp = 250
		tlist = [0 for x in range(512)]
		for x in tmp:
			tlist[x] = tmp[x]
		tmp = tlist
		for it in jiang:
			tmpt = tmp[:]
			for p in it:
				tmpt[p] -= 1
			rst += map(lambda x: [it] + x, hu(keys, len(ls) - 2, jingp, tmpt)) 
		return rst


if __name__ == '__main__':
	print '11111111111111111111111111111111111111111111111111111111111'
	import cProfile, pstats
  
	#tt = profile.runcall("huex([250, 43, 43, 42, 42, 41, 41, 26, 26, 5, 4, 3, 3, 3])", "timeit")
		
	'''
	tmp = hu([250, 42, 42, 41, 41, 26, 26, 5, 4, 3, 3, 3])
	for x in tmp:
		print x 

	'''

	pro = cProfile.Profile()
	tt = pro.runcall(huex, [250, 250, 250, 250, 250, 41, 41, 26, 26, 5, 4, 3, 3, 3])
	print 'cProfile', tt
	
	pro.print_stats()
	
	import time

	t = time.time()
	for i in range(250):
		tmp = huex([7, 47, 47, 47, 29, 29, 29, 25, 24, 23, 7, 7, 5, 5])
	print '%.6f' % ((time.time() - t) / 250.0)
	for x in tmp:
		print x
	print cut

	t = time.time()
	for i in range(250):
		tmp = huex([250, 43, 43, 42, 42, 41, 41, 26, 26, 5, 4, 3, 3, 3])
	print '%.6f' % ((time.time() - t) / 250.0)
	for x in tmp:
		print x     
	print cut


	t = time.time()
	for i in range(250):
		tmp = huex([250, 250, 81, 81, 47, 46, 26, 25, 7, 6, 5, 4, 4, 4])
	print '%.6f' % ((time.time() - t) / 250.0)
	for x in tmp:
		print x
	print cut

	t = time.time()
	for i in range(250):
		tmp = huex([250, 250, 250, 250, 250, 27, 27, 26, 26, 25, 25, 24, 24, 24])
	print '%.6f' % ((time.time() - t) / 250.0)
	print len(tmp)
	for x in tmp:
		print x
		

	print cut
