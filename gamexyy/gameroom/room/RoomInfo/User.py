#coding:utf8


from room.lib.RedisManager import rdsmanager
import json
from firefly.server.globalobject import GlobalObject


USER_NONE = 0
USER_READY = 1
USER_LOOK = 2
USER_SIT = 3


class User:
    '''用户类'''

    def __init__(self, userid, sessionid = ''):
        '''

        '''
        self.userid    = userid
        
        self.money = 0 
        self.exp = 0
        self.nikename = ''
        self.username = ''
        self.skey = ''    #密码


        self.deskno    = -1
        self.deskstation = -1
        self.state     = -1
        self.isPlaying = False # 是否做游戏中
        self.online = True  #是否在线
        

        stmp = sessionid.split(',')

        self.sessionid = sessionid
        self.servername = stmp[0]
        self.sid = int(stmp[1])

        self.rds = rdsmanager.get_client(self.userid)
        self.rkey = 'hashuser:%s' % userid

    def __eq__(self, other):
        if other is None:
            return False
        return self.userid == other.userid


    def get_user_info_rds(self):
        return self.rds.hgetall(self.rkey)


    def update_user_info(self, userinfo):
        self.money          = int(userinfo.get("money", 0))
        self.username       = userinfo.get("username", '')
        self.nikename       = userinfo.get("nikename", '')
        self.exp            = int(userinfo.get("exp", 0))
        self.skey           = userinfo.get("skey", '')


    def update_user_info_rds(self):
        info = self.get_user_info_rds()
        self.update_user_info(info)


    def change_point(self, money, rdschg = True):
        self.my_money = self.my_money + money
        if self.my_money <= 0:
            self.my_money = 0
            self.rds.hset(self.rkey, 'money', money)
        if rdschg:
            self.rds.hincrby(self.rkey, 'money', money)

    def add_exp(self, exp, rdschg = True):
        self.exp += self.exp
        if rdschg:
            self.rds.hincrby(self.rkey, 'exp', exp)


    def __str__(self):

        tmp = self.__dict__.copy()
        del tmp['rds']

        return json.dumps(tmp)


    def get_skey(self):
        return self.skey

    def get_exp(self):
        return self.exp

    def getUserID(self):
        return self.userid

    def getServerName(self):
        return self.servername

    def getSID(self):
        return self.sid

    def getSessionid(self):
        return self.sessionid

    def getUserName(self):
        '''获取账号名
        '''
        return self.name

    def getUserState(self):
        return self.state

    def setUserState(self, state):
        self.state = state

    def disconnectClient(self):
        '''断开'''
        # msg = "您账户其他地方登录"
        pass

    def sit(self,  deskno,  deskindex):
        self.deskno = deskno
        self.deskindex = deskindex

    def getsit(self):
        return [self.deskno, self.deskindex]


    def getIsPlay(self):
        return self.isPlaying


    def sendMessage(self, msgid, msg):
        servername, sid = self.getServerName(), self.getSID()
        GlobalObject().root.callChildByName(servername, 'remote_pushMessage', msgid, msg, [sid])


    def loseConnection(self):
        servername, sid = self.getServerName(), self.getSID()
        GlobalObject().root.callChildByName(servername, 'remote_loseConnection', [sid])