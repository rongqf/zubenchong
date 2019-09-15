#coding:utf8


from msghander import addhander

from room.lib.RedisManager import rdsmanager
from room.RoomInfo.User import User
from room.RoomInfo.UserManager import usersManager
import json


@addhander
def login_100(sessionid, cmdid, data):
    data = json.loads(data)

    userid = data.get('userid')
    skey = data.get('skey')

    if userid and skey:
        tmp = User(userid, sessionid)
        tmp.update_user_info_rds()
        
        if tmp.get_skey() == skey:
            usersManager.addUser(tmp)
            return str(tmp)
        else:
            return json.dumps({'ret':0, 'desc':'skey error'})
    
    else:
        return json.dumps({'ret':0, 'desc':'data error'})
