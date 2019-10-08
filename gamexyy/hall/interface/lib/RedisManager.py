import redis

class Singleton(type):
    """Singleton Metaclass"""
    
    def __init__(self, name, bases, dic):
        super(Singleton, self).__init__(name, bases, dic)
        self.instance = None
        
    def __call__(self, *args, **kwargs):
        if self.instance is None:
            self.instance = super(Singleton, self).__call__(*args, **kwargs)
        return self.instance


        
class RedisManager(object):
    __metaclass__ = Singleton

    def __init__(self):
        self.__allredis = []
        pool = redis.ConnectionPool(host = '127.0.0.1', port = 25000,
                     db = 0, password = 'rqf123456!@#$%^&*')
        client = redis.Redis(connection_pool = pool)
        self.add_client(client)             

    def add_client(self, redis):
        self.__allredis.append(redis)

    def get_client(self, idx = 0):
        if idx >= len(self.__allredis):
            idx = idx % len(self.__allredis)
        if idx < 0 or idx > len(self.__allredis) - 1:
            return None
        return self.__allredis[idx]
    

rdsmanager = RedisManager()

if __name__ == '__main__':
        
        client = rdsmanager.get_client()

        x = 'aaaaa'#{'a':1, 'b':2}
        client.set('guo', x)

        client.hset('myhash','field1',"foo")
        hashVal = client.hget('myhash','field1')

        hmDict={'a':19999,'b':2}

        client.hmset('hash1',hmDict)


        client.hincrby('hash1','b', 3)

        val = client.hgetall('hash1')

        print "Get hmset value:",val


        print hashVal
