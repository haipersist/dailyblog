#-*-coding:utf-8-*-

"""
    cache.py
    the cache is used to cache some view functions inorder to
    avoid wasting resources when requesting the same one  and lower visit time
    in short serid time.


 :copyright: (c) 2017 by Haibo Wang.
"""


import functools
import hashlib
import logging
from django.core.cache import caches






logger = logging.getLogger(__name__)



class Cache(object):
    """
    I use proxy design pattern to write the class.
    the Cache is the proxy of django cache.
    It can do all that django cache does.
    In additions,it provides a decorator usdt to
    decorate view function.

    """
    def __init__(self,cache_type='memcache'):
        self._set_cache(cache_type)

    def _set_cache(self,cache_type):
        self.cache = caches[cache_type]

    def get(self,key,default=None):
        #Proxy function for some cache
        return self.cache.get(key,default=default)

    def set(self, key, value,timeout=500):
        #Proxy function for some cache
        self.cache.set(key, value,timeout=timeout)

    def delete(self,key):
        #Proxy function for some cache
        self.cache.delete(key)

    def get_many(self,keys):
        return self.cache.get_many(keys)

    def clear(self):
        #Proxy function for some cache
        self.cache.clear()

    def close(self):
        self.cache.close()


    def create_cache_key(self,key):
        return hashlib.md5(key).hexdigest()

    def cached(self,timeout=300):
        """
        decorator for view functions

        :param timeout:the expire time for some view function
        :return: the decorator
        """
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args,**kwargs):
                try:
                    cache_key = self.create_cache_key(repr((func,args,kwargs)))
                    rv = self.cache.get(cache_key)
                except Exception:
                    logger.exception('Exception possibly due to cache backend.')
                    return func(*args,**kwargs)
                if not rv:
                    rv = func(*args,**kwargs)
                    try:
                        self.cache.set(cache_key,rv,timeout)
                    except Exception:
                        logger.exception('Exception possibly due to cache backend.')
                        return rv
                return rv

            return wrapper
        return decorator




