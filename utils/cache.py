#-*-coding:utf-8-*-

"""
    cache.py
    the cache is used to cache some view functions inorder to avoid wasting resources when requesting the same one
    in short serid time.


"""


import functools
import hashlib
import logging
from time import time
from django.core.cache import caches


logger = logging.getLogger(__name__)


try:
    import cPickle as pickle
except ImportError:  # pragma: no cover
    import pickle



class Cache(object):

    def __init__(self):
        self._set_cache()

    def _set_cache(self):
        try:
            self.cache = caches['memcache']
        except:
            self.cache = caches['default']

    def get(self,*args,**kwargs):
        #Proxy function for some cache
        self.cache.get(*args,**kwargs)

    def set(self,*args, **kwargs):
        #Proxy function for some cache
        self.cache.set(*args, **kwargs)

    def delete(self,key):
        #Proxy function for some cache
        pass

    def clear(self):
        #Proxy function for some cache
        pass

    def create_cache_key(self,key):
        return hashlib.md5(key).hexdigest()

    def cached(self,timeout=None):
        #decorator for view functions
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




