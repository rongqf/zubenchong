#coding:utf8
'''
Created on 2013-5-8

@author: lan (www.9miao.com)
'''

from dbpool import dbpool
from MySQLdb.cursors import DictCursor
from numbers import Number
import logging

logger = logging.getLogger('hell')



def forEachPlusInsertProps(tablename,props):
    assert type(props) == dict
    pkeysstr = str(tuple(props.keys())).replace('\'','`')
    pvaluesstr = ["%s,"%val if isinstance(val,Number) else 
                  "'%s',"%str(val).replace("'", "\\'") for val in props.values()]
    pvaluesstr = ''.join(pvaluesstr)[:-1]
    sqlstr = """INSERT INTO `%s` %s values (%s);"""%(tablename,pkeysstr,pvaluesstr)
    return sqlstr

def FormatCondition(props):
    """生成查询条件字符串
    """
    items = props.items()
    itemstrlist = []
    for _item in items:
        if isinstance(_item[1],Number):
            sqlstr = " `%s`=%s AND"%_item
        else:
            sqlstr = " `%s`='%s' AND "%(_item[0],str(_item[1]).replace("'", "\\'"))
        itemstrlist.append(sqlstr)
    sqlstr = ''.join(itemstrlist)
    return sqlstr[:-4]

def FormatUpdateStr(props):
    """生成更新语句
    """
    items = props.items()
    itemstrlist = []
    for _item in items:
        if isinstance(_item[1],Number):
            sqlstr = " `%s`=%s,"%_item
        else:
            sqlstr = " `%s`='%s',"%(_item[0],str(_item[1]).replace("'", "\\'"))
        itemstrlist.append(sqlstr)
    sqlstr = ''.join(itemstrlist)
    return sqlstr[:-1]
    
def forEachUpdateProps(tablename,props,prere):
    '''遍历所要修改的属性，以生成sql语句'''
    assert type(props) == dict
    pro = FormatUpdateStr(props)
    pre = FormatCondition(prere)
    sqlstr = """UPDATE `%s` SET %s WHERE %s;"""%(tablename,pro,pre) 
    return sqlstr

def EachQueryProps(props):
    '''遍历字段列表生成sql语句
    '''
    sqlstr = ""
    if props == '*':
        return '*'
    elif type(props) == type([0]):
        for prop in props:
            sqlstr = sqlstr + prop +','
        sqlstr = sqlstr[:-1]
        return sqlstr
    else:
        raise Exception('props to query must be dict')
        return

def forEachQueryProps(sqlstr, props):
    '''遍历所要查询属性，以生成sql语句'''
    if props == '*':
        sqlstr += ' *'
    elif type(props) == type([0]):
        i = 0
        for prop in props:
            if(i == 0):
                sqlstr += ' ' + prop
            else:
                sqlstr += ', ' + prop
            i += 1
    else:
        raise Exception('props to query must be list')
        return
    return sqlstr


def ReadDataFromDB(tablename):
    """
    """
    sql = """select * from %s"""%tablename
    conn = dbpool.connection()
    cursor = conn.cursor(cursorclass = DictCursor)
    result = None
    try:
        count = cursor.execute(sql)
        result=cursor.fetchall()
    except Exception,e:
        logger.error(e)
        logger.error(sql)
    
    cursor.close()
    conn.close()
    return result

def DeleteFromDB(tablename,props):
    '''从数据库中删除
    '''
    prers = FormatCondition(props)
    sql = """DELETE FROM %s WHERE %s ;"""%(tablename,prers)
    conn = dbpool.connection()
    cursor = conn.cursor()
    count = 0
    try:
        count = cursor.execute(sql)
        conn.commit()
    except Exception,e:
        logger.error(e)
        logger.error(sql)
    cursor.close()
    conn.close()
    return bool(count)

def InsertIntoDB(tablename,data):
    """写入数据库
    """
    sql = forEachPlusInsertProps(tablename,data)
    conn = dbpool.connection()
    cursor = conn.cursor()
    count = 0
    try:
        count = cursor.execute(sql)
        conn.commit()
    except Exception,e:
        logger.error(e)
        logger.error(sql)
    cursor.close()
    conn.close()
    return bool(count)

def UpdateWithDict(tablename,props,prere):
    """更新记录
    """
    sql = forEachUpdateProps(tablename, props, prere)
    conn = dbpool.connection()
    cursor = conn.cursor()
    count = 0
    try:
        count = cursor.execute(sql)
        conn.commit()
    except Exception,e:
        logger.error(e)
        logger.error(sql)
    cursor.close()
    conn.close()
    if(count >= 1):
        return True
    return False


def GetOneRecordInfo(tablename,props):
    '''获取单条数据的信息
    '''
    props = FormatCondition(props)
    sql = """Select * from `%s` where %s"""%(tablename,props)

    conn = dbpool.connection()
    cursor = conn.cursor(cursorclass = DictCursor)
    result = None

    try:
        count = cursor.execute(sql)
        result=cursor.fetchone()
    except Exception,e:
        logger.error(e)
        logger.error(sql)
        
    cursor.close()
    conn.close()
    return result

def GetAllRecordInfo(tablename,props):
    '''获取单条数据的信息
    '''
    props = FormatCondition(props)
    sql = """Select * from `%s` where %s"""%(tablename,props)

    conn = dbpool.connection()
    cursor = conn.cursor(cursorclass = DictCursor)

    result = None

    try:
        count = cursor.execute(sql)
        result=cursor.fetchall()
    except Exception,e:
        logger.error(e)
        logger.error(sql)
        
    cursor.close()
    conn.close()
    return result

def execsql(sql):
    """
    """
    conn = dbpool.connection()
    cursor = conn.cursor(cursorclass = DictCursor)
    result = None
    try:
        count = cursor.execute(sql)
        result=cursor.fetchall()
    except Exception,e:
        logger.error(e)
        logger.error(sql)
    
    cursor.close()
    conn.close()
    return result

def execsqlcommit(sql):
    """
    """
    conn = dbpool.connection()
    cursor = conn.cursor(cursorclass = DictCursor)
    result = None
    count = 0
    try:
        count = cursor.execute(sql)
        conn.commit()
        #cursor.callproc('ReqFriend', (7, 12))
        #print(1, sql)
        #result=cursor.fetchall()


    except Exception,e:
        logger.error(e)
        logger.error(sql)
    
    cursor.close()
    conn.close()
    if(count >= 1):
        return True
    return False

def executemany(sql, data):
    """
    """
    conn = dbpool.connection()
    cursor = conn.cursor()
    result = None
    count = 0
    try:
        count = cursor.executemany(sql, data)
        print('executemany', sql, data)
        conn.commit()
    except Exception,e:
        logger.error(e)
        logger.error(sql)
    
    cursor.close()
    conn.close()
    if(count >= 1):
        return True
    return False

if __name__ == '__main__':


    sqlcfg = {'host':"127.0.0.1",
    'user':'root',
    'passwd':'112233',
    'db':'gamedb',
    'port':3306,
    'charset':'utf8'}
    dbpool.initPool(**sqlcfg)

    sql = "CALL GetFriendAcc(7)"
    print execsqlcommit(sql)


    sql = "CALL ReqFriend(%d, %d)"
    sql = sql % (7, 12)
    print execsqlcommit(sql)

    print FormatCondition({'id' : 1})

    import time
    t = time.time()
    for i in range(1):
        GetAllRecordInfo('sys_config', {'id': 1})
    print time.time() - t


    
