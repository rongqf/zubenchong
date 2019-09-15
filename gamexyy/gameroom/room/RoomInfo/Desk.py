#coding:utf8


import json
import User
import importlib
#import room.game.game_1000


class Desk:
    '''用户类'''

    def __init__(self, deskid, usercut, gameid):
        '''

        '''
        self.deskid    = deskid
        self.users = [None for _ in range(usercut)]
        self.lookusers =  [[] for _ in range(usercut)]
        self.isPlaying = False
        self.game = importlib.import_module(r'room.game.game_%d.GameMain' % gameid).Game()

    def usersit(self, user, index):
        if index < len(self.users):
            self.users[index] = user
            user.set(self.deskid, index)

    def userup(self, index):
        self.users[index] = None

    def userready(self, index):
        if self.users[index]:
            self.users[index].setUserState(User.USER_READY)

    def __str__(self):

        tmp = self.__dict__.copy()
        return json.dumps(tmp)


    def getIsPlay(self):
        return self.isPlaying

    def getUserCut(self):
        return len(filter(lambda x: x != None, self.users))

    def sendMessage(self, msgid, msg):

        us = self.users
        for p in self.lookusers:
            us += p

        for user in us:
            user.sendMessage(msgid, msg)