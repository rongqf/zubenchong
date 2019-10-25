#coding:utf8

import json, time, datetime

import sqlutil
import logging
logger = logging.getLogger('hell')


def get_friend(userid):
	#sql = "CALL GetFriend('%d');"
	sql = r'SELECT f.friendid, u.username, u.exp, u.logo FROM friend f JOIN userinfo u on f.friendid = u.userid where f.userid = %d;'
	sql = sql % userid
	return sqlutil.execsql(sql)

def get_friendreq(userid):
	#sql = "CALL GetFriendReq('%d');"
	sql1 = '''SELECT f.requid, f.accuid, f.acccode, u.username 
	FROM friendreq f JOIN userinfo u on f.accuid = u.userid 
	WHERE f.requid = %d and f.acccode <> 0 and f.valid = 1;'''
	sql1 = sql1 % userid
	ret = sqlutil.execsql(sql1)

	sql2 = '''UPDATE friendreq SET valid = 0 
	WHERE requid = %d and acccode <> 0 and valid = 1;'''
	sql2 = sql2 % userid
	sqlutil.execsqlcommit(sql2)

	return ret


def get_friendacc(userid):
	sql = '''SELECT f.requid, f.accuid, f.acccode, u.username 
	FROM friendreq f JOIN userinfo u on f.requid = u.userid 
	WHERE f.accuid = %d and f.acccode = 0 and f.valid = 1;'''

	sql = sql % userid
	return sqlutil.execsql(sql)

def req_friend(userid, friendid):
	tmp = sqlutil.GetOneRecordInfo('friend', {'userid': userid, 'friendid' : friendid})
	if tmp:
		return {'des': 'error friend is exist'}

	tmp = sqlutil.GetOneRecordInfo('friendreq', {'requid': userid, 'accuid' : friendid})
	if tmp and tmp['acccode'] != 2:
		return {'des': 'error friendreq is exist'}

	if not tmp:
		sqlutil.InsertIntoDB('friendreq', {'requid':userid, 'accuid':friendid, 'reqtime': datetime.datetime.now()})
	else:
		sqlutil.UpdateWithDict('friendreq', {'acccode': 0, 'valid' : 1, 'reqtime': datetime.datetime.now()}, {'requid': userid, 'accuid' : friendid})

	return {'des': 'ok'}

#code=1接受，2拒绝
def acc_friend(userid, friendid, code):
	tmp = sqlutil.GetOneRecordInfo('friendreq', {'requid': userid, 'accuid' : friendid})
	if not tmp:
		return {'des': 'error record not exist'}
	if tmp['acccode'] != 0:
		return {'des': 'error db acccode error'}

	sqlutil.UpdateWithDict('friendreq', {'acccode': code}, {'requid': userid, 'accuid' : friendid})
	if code == 1:
		sqlutil.InsertIntoDB('friend', {'userid':userid, 'friendid':friendid})
		sqlutil.InsertIntoDB('friend', {'userid':friendid, 'friendid':userid})
		#sqlutil.execsqlcommit('INSERT ignore INTO friend(userid, friendid) VALUES(%d, %d)' % (userid, friendid))
		#sqlutil.execsqlcommit('INSERT ignore INTO friend(userid, friendid) VALUES(%d, %d)' % (friendid, userid))

	return {'des': 'ok'}

if __name__ == '__main__':
	from dbpool import dbpool

	sqlcfg = {'host':"127.0.0.1",
	'user':'root',
	'passwd':'112233',
	'db':'gamedb',
	'port':3306,
	'charset':'utf8'}

	dbpool.initPool(**sqlcfg)



	print(get_friend(7))
	print(get_friendacc(7))
	print(get_friendreq(7))
	print(get_friend(12))
	print(get_friendacc(12))
	print(get_friendreq(12))
	print(req_friend(7, 12))
	print(acc_friend(7, 12, 1))