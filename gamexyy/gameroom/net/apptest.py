#coding:utf8


from twisted.web import resource
from twisted.internet import reactor, defer
from twisted.python import log
from firefly.server.globalobject import GlobalObject, netserviceHandle, webserviceHandle, remoteserviceHandle
from firefly.utils.services import CommandService
import time
import sys, json
from firefly.server.logobj import loogoo

import websocket

class NetCommandService(CommandService):
    def callTargetSingle(self,targetKey,*args,**kw):
        self._lock.acquire()
        try:
            target = self.getTarget(0)
            if not target:
                log.err('the command '+ str(targetKey) + ' not Found on service')
                return None
            if targetKey not in self.unDisplay:
                # log.msg("call method %s on service[single]"%target.__name__)
                pass
            defer_data = target(targetKey, *args, **kw)
            if not defer_data:
                return None
            if isinstance(defer_data, defer.Deferred):
                return defer_data
            d = defer.Deferred()
            d.callback(defer_data)
        finally:
            self._lock.release()
        return d

###########################################################################################

msgdistribute = GlobalObject().json_config.get("msgdistribute")
msgrule = msgdistribute.get('rule')
msgdefault = msgdistribute.get('default')
servername = GlobalObject().json_config.get("name")
iswebsocket = GlobalObject().json_config.get("iswebsocket", False)
if iswebsocket:
    GlobalObject().netfactory.protocol = websocket.WebSocketHandler
logpath = GlobalObject().json_config.get('log')
servername = GlobalObject().json_config.get('name')
if logpath:
    if logpath:
        log.addObserver(loogoo(logpath))#日志处理
    log.startLogging(sys.stdout)

###########################################################################################
    
netservice = NetCommandService("loginService")
GlobalObject().netfactory.addServiceChannel(netservice)

class Session:
    def __init__(self, sid, servename):
        self.session = '%s,%d' % (servename, sid)

    def getsession(self):
        return self.session

    def __str__(self):
        return self.session

class SessionService:
    def __init__(self):
        self.sessions = {}

    def add(self, sid, session):
        if self.sessions.get(sid):
            del self.sessions[sid]
        self.sessions[sid] = session

    def delete(self, sid):
        if self.sessions.get(sid):
            del self.sessions[sid]

    def getbysid(self, sid):
        return self.sessions.get(sid)

@netserviceHandle
def handmsg_0(cmdid, _conn, data):
    sid = _conn.transport.sessionno
    session = sessionService.getbysid(sid)
    return handmsg(cmdid, session, data)
    

@defer.inlineCallbacks
def handmsg(cmdid, session, data):
    remotename = msgdefault
    if msgrule:
        for k in msgrule:
            if cmdid in msgrule[k]:
                remotename = k
                break

    sessionid = session.getsession()
    begintm = time.clock()
    msg = yield GlobalObject().remote[remotename].callRemote("handlegamemsg", sessionid, cmdid, data)
    endtm = time.clock()
    calltm = endtm - begintm
    log.msg("%s rpclog: %s %s %s %s %s %s %s" % (servername, sessionid, begintm, endtm, calltm, cmdid, data, msg))
    defer.returnValue(msg)
    

sessionService = SessionService()
def doConnectionMade(_conn):
    sid = _conn.transport.sessionno
    session = Session(sid, servername)
    sessionService.add(sid, session)
    log.msg("doConnectionMade: %s " % session)

def doConnectionLost(_conn):
    sid = _conn.transport.sessionno
    session = sessionService.getbysid(sid)
    handmsg(99, session, None)
    sessionService.delete(sid)
    log.msg("doConnectionLost: %s " % session)



GlobalObject().netfactory.doConnectionMade = doConnectionMade
GlobalObject().netfactory.doConnectionLost = doConnectionLost
###########################################################################################

def remoteserviceHandleAll(target):
    for x in GlobalObject().remote:
        GlobalObject().remote[x]._reference._service.mapTarget(target)


@remoteserviceHandleAll
def remote_pushMessage(msgid, msg, sendList):
    log.msg('pushmsg: msgid: %s, msg: %s, sendList: %s' % (msgid, msg, sendList))
    GlobalObject().netfactory.pushObject(msgid, msg, sendList)


@remoteserviceHandleAll
def remote_loseConnection(loselist):
    log.msg('loseConnection: loselist: %s' % loselist)
    for x in loselist:
        GlobalObject().netfactory.loseConnection(x)


###########################################################################################

@webserviceHandle()
class webapi(resource.Resource):
    def render(self, request):
        return "webapi" + str(GlobalObject().webroot.listNames())


@webserviceHandle()
class getconfig(resource.Resource):
    def render(self, request):
        return json.dumps(GlobalObject().json_config)
