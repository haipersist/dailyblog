# -*- coding: utf-8 -*-


import redis
from . import BaseConfig


class BaseRedis(BaseConfig):


    def __init__(self):
        super(BaseRedis,self).__init__()
        self._connect()


    def _connect(self):
        config = self.settings['redis']
        self.host, self.port = config['HOST'],config['PORT']

        #Implemention of Redis Protocol,this abstract class
        #provides a pythoninterface to all Redis cmds.
        self.rs = redis.StrictRedis(self.host,
                                     port=self.port,
                                     #password=self.password,
                                     )

    def set(self,name,data,expire=3600*20):
        """
        :param name:
        :param data: data can be any structure,dict,list,tuple,set and string.
        For every single type,use corresponding store method.
        :return:
        """
        if isinstance(data,(basestring,bytes)):
            self.rs.set(name,data)
        elif isinstance(data,list or tuple):
            for item in data:
                #add item from right side.
                self.rs.rpush(name,item)
        elif isinstance(data,set):
            for item in data:
                self.rs.sadd(name,item)
        elif isinstance(data,dict):
            self.rs.hmset(name,data)
        if not isinstance(expire,int):
            expire = 3600*24
        self.rs.expire(name, expire)


    def get(self,name,type='string'):
        if type == 'string':
            result = self.rs.get(name)
        elif type == 'list' or type == 'tuple':
            result = self.rs.lrange(name,0,-1)
        elif type == 'dict':
            result = self.rs.hgetall(name)
        elif type == 'set':
            result = self.rs.smembers(name)

        return result



def test():
    client=BaseRedis()
    #client.rs.delete('qw')
    client.set('test',['sq'])
    print len(client.get('latest_jobs',type='list'))

    print client.rs.llen('new_company')









if __name__=="__main__":
    test()


