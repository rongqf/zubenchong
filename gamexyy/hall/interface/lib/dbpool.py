#coding:utf8
'''
Created on 2013-5-8

@author: lan (www.9miao.com)
'''
from DBUtils.PooledDB import PooledDB
import MySQLdb

DBCS = {'mysql':MySQLdb,}

class DBPool(object):
    '''
    '''
    def initPool(self,**kw):
        '''
        '''
        self.config = kw
        creator = DBCS.get(kw.get('engine','mysql'),MySQLdb)
        self.pool = PooledDB(creator,5,**kw)
        
    def connection(self):
        return self.pool.connection()

dbpool = DBPool()

if __name__ == '__main__':

    aa = {'host':"localhost",
    'user':'root',
    'passwd':'112233',
    'db':'gamexyy',
    'port':3306,
    'charset':'utf8'}
    dbpool.initPool(**aa)

    con = dbpool.connection()
    cursor = con.cursor(cursorclass = MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT VERSION()")
    data = cursor.fetchall()
    cursor.close()
    con.close()
    print data
