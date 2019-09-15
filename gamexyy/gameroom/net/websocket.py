
#coding:utf8

from twisted.python import log
from TwistedWebsocket.server import Protocol

from twisted.internet import  reactor


def DefferedErrorHandle(e):
    '''延迟对象的错误处理'''
    log.err(str(e))
    return

class WebSocketHandler(Protocol):
    def onHandshake(self, header):
    	pass
        #g = re.search('Origin\s*:\s*(\S+)', header)
        #if not g: return
        #print "\n[HANDSHAKE] %s origin : %s" % (self.id, g.group(1)) 

    def onConnect(self):
        '''连接建立处理
        '''
        log.msg('Client %d login in.[%s,%d]'%(self.transport.sessionno,\
                self.transport.client[0],self.transport.client[1]))
        self.factory.connmanager.addConnection(self)
        self.factory.doConnectionMade(self)

    def onDisconnect(self):
        '''连接断开处理
        '''
        log.msg('Client %d login out.'%(self.transport.sessionno))
        self.factory.doConnectionLost(self)
        self.factory.connmanager.dropConnectionByID(self.transport.sessionno)


    def onMessage(self, msg):
        '''数据到达处理
        @param data: str 客户端传送过来的数据
        '''
        index = msg.find('|')
        if index >= 0:
        	command = int(msg[:index])
        	request = msg[index + 1:]
        	
	        d = self.factory.doDataReceived(self,command,request)
	        

	        if d:
                    d.addCallback(self.safeToWriteData,command)
                    d.addErrback(DefferedErrorHandle)

    def safeToWriteData(self, data, command):
        '''线程安全的向客户端发送数据
        @param data: str 要向客户端写的数据
        '''    
        if not self.transport.connected or data is None:
            return
        senddata = '%s|%s' % (command, data)
        reactor.callFromThread(self.sendMessage,senddata)
                
