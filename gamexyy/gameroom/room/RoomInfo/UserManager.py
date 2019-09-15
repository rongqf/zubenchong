#coding:utf8
'''

'''
from firefly.utils.singleton import Singleton
from firefly.server.globalobject import GlobalObject
from twisted.internet import reactor

import logging
servername = GlobalObject().json_config.get('name')
logger = logging.getLogger(servername)

class UsersManager:

    __metaclass__ = Singleton

    def __init__(self):
        self._users = {}
        self._userId = {}

    def addUser(self, user):
        """添加一个用户
        """
        sessionid = user.getSessionid()
        userid = user.getUserID()

        logger.info('addUser %s', user)


        olduser = self.getUserByUserID(userid)
        if olduser:
            olduser.sendMessage(199, '强登')
            olduser.loseConnection()
            self.dropUserByUserID(userid)


        self._users[sessionid] = user
        self._userId[userid] = sessionid

        return user

    def disconnectBySessionID(self, sessionid):
        user = self.getUserBySessionID(sessionid)
        if user:
            logger.info('disconnectBySessionID %s', user)
            if not user.getIsPlay():
                userid = user.getUserID()
                self.dropUserByUserID(userid)

    def getUserBySessionID(self, sessionid):
        return self._users.get(sessionid)

        
    def getUserByUserID(self, UserID):
        """根据用户ID获取用户信息
        """
        sessionid = self._userId.get(UserID)
        return self.getUserBySessionID(sessionid)

    def dropUser(self, user):
        """处理用户下线
        """
        sessionid = user.getSessionid()
        userid = user.getUserID()

        if sessionid in self._users:
            del self._users[sessionid]

        if userid in self._userId:
            del self._userId[userid]

    def dropUserByUserID(self, UserID):
        """根据用户ID处理用户下线
        """
        user = self.getUserByUserID(UserID)
        if user:
            logger.info('dropUserByUserID %s', user)
            self.dropUser(user)


    def getUsersCount(self):
        '''获取在线用户数'''
        return len(self._users)

    def showCurrentOnlinePlayerCount(self):
        player_count = self.getUsersCount()
        logger.info('current online player count:%d', player_count)
        reactor.callLater(60, self.showCurrentOnlinePlayerCount)
        
    def __str__(self):
        return r'\r\n'.join([str(x) for x in self._users.values()])


    def getUsersManagerInfo(self):
        return {'sidlen':len(self._users), 'uidlen': len(self._userId)}


    def sendMessageByUserID(self, msgid, msg, idlist):
        tmp = {}
        for uid in idlist:
            user = self.getUserByUserID(uid)
            servername, sid = self.getServerName(), self.getSID()
            tmp[servername] = tmp.get(servername, [])
            tmp[servername].append(sid)

        for sname in tmp:
            GlobalObject().root.callChildByName(sname, 'remote_pushMessage', msgid, msg, tmp[sname])

usersManager = UsersManager()