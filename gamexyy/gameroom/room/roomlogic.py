#coding:utf8

import sys, time, json
from twisted.web import resource
from firefly.server.globalobject import GlobalObject, webserviceHandle, rootserviceHandle
from twisted.python import log

import lib.xxylog
import MessageComponents
from RoomInfo.UserManager import usersManager
from RoomInfo.DeskManager import deskManager



logpath = GlobalObject().json_config.get('log')
servername = GlobalObject().json_config.get('name')
logger = lib.xxylog.addloghander(servername, '.\\logs\\')

if logpath:
    log.addObserver(lib.xxylog.loogoo(logger))#日志处理
    log.startLogging(open(logpath, 'w+'), setStdout=0)


@webserviceHandle()
class allapi(resource.Resource):
    def render(self, request):
        return "webapi" + str(GlobalObject().webroot.listNames())


@webserviceHandle()
class getglobals(resource.Resource):
    def render(self, request):
        return str(globals())
    
@webserviceHandle()
class userinfo(resource.Resource):
    def render(self, request):
        return str(usersManager)

@rootserviceHandle
def handlegamemsg(sessionid, cmdid, data):

    begintm = time.clock()
    if cmdid in MessageComponents.msghander.msghander:
        
        msg = MessageComponents.msghander.msghander[cmdid](sessionid, cmdid, data)
        endtm = time.clock()
        usetm = endtm - begintm
        
        logger.debug(json.dumps([sessionid, cmdid, data,  begintm, endtm, usetm, msg]))
        
        return msg
    else:
        logger.error('msgid:%d not have hander' % cmdid)

    


