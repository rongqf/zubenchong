#coding:utf8


from msghander import addhander

from room.lib.RedisManager import rdsmanager
from room.RoomInfo.User import User
from room.RoomInfo.UserManager import usersManager
import json


@addhander
def login_101(sessionid, cmdid, data):
    
    user = usersManager.getUserBySessionID(sessionid)
    uid = user.getUserID()

    