#coding:utf8


from firefly.utils.singleton import Singleton

import Desk

class DeskManager:
    '''用户类'''
    __metaclass__ = Singleton

    def __init__(self, deskcut, usercut, gameid):
        '''

        '''
        self.desks = [Desk.Desk(i, usercut, gameid) for i in range(deskcut)]

    def getDesk(self, index):
        if index < len(self.desks):
            return self.desks[index]
        return None

    def getNullDesk(self):
        for d in self.desks:
            if d.getUserCut() == 0:
                return d
        return None

deskManager = DeskManager(1, 2, 1000)