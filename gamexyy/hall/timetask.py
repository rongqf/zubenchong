import time

from interface.lib.dbpool import dbpool
from interface.lib.RedisManager import rdsmanager
from interface.lib import sqlutil
import logging



sqlcfg = {'host':"127.0.0.1",
    'user':'root',
    'passwd':'112233',
    'db':'gamedb',
    'port':3306,
    'charset':'utf8'}
dbpool.initPool(**sqlcfg)

updatesql = 'UPDATE userinfo SET gamepoint = %s, exp = %s WHERE userid = %s'
filds = ['gamepoint', 'exp', 'userid']

def WriteChangeUserIDs():
	try:
		rds = rdsmanager.get_client()
		userids = rds.smembers('setupdateuser')
		nline = 100
		cut = len(userids) / nline + 1

		if len(userids) > 0:
			userids = list(userids)
			for i in range(cut):
				tmp = userids[i * nline: (i + 1) * nline]

				pipe = rds.pipeline()
				for p in tmp:
					rkey = 'hashuser:%s' % p
					pipe.hmget(rkey, filds)
				userinfos = pipe.execute()
				userinfos = [(int(p[0]), int(p[1]), int(p[2])) for p in userinfos]
				print(userinfos)
				sqlutil.executemany(updatesql,  userinfos)
				tmp = [int(p) for p in tmp]
				print tmp
				rds.srem('setupdateuser', *tmp)

	except Exception as e:
		print(e)

	

	
if __name__ == '__main__':
	lasttm = 0
	while True:
		if time.time() - lasttm > 60 * 5:
			lasttm = time.time()
			WriteChangeUserIDs()
		time.sleep(0.1)

	