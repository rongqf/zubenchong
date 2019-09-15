# -*- coding: utf8 -*-

import tornado.web

from lib.RedisManager import rdsmanager
from lib import sqlutil


    
def handle(param):

    ret = 1    
    tmp = sqlutil.ReadDataFromDB('servernodelist')
        
    return {'ret':ret, 'data':tmp}
