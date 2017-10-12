#-*-coding:utf-8 -*-
__author__ = 'wanghb311'


MYSQL_DB = 'app_dailyblog'
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'admin'
MYSQL_PORT = 3306
MYSQL_HOST = '127.0.0.1'


REDIS_PORT = 6379
REDIS_HOST = '127.0.0.1'


DATABASES = {
    'mysql': {
        'NAME': MYSQL_DB,#数据库名称
        'USER':MYSQL_USER,
        'PASSWORD':MYSQL_PASSWORD,
        'PORT':MYSQL_PORT,
        'HOST':MYSQL_HOST,
    },
    'redis': {
        'PORT':REDIS_PORT,
        'HOST':REDIS_HOST,
    },
}

#DATABASES = pickle.dumps(DATABASES)



