#coding:utf8


from msghander import addhander

from room.lib.RedisManager import rdsmanager
from room.RoomInfo.User import User
from room.RoomInfo.UserManager import usersManager
import json


@addhander
def disconnect_99(sessionid, cmdid, data):
    usersManager.disconnectBySessionID(sessionid)

