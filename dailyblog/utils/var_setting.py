from __future__ import unicode_literals
#-*-coding:utf-8 -*-
"""

the module can set some necessary config,and the setting class have

some userful methods.

Class:
  Settings

Func:
   get_project_settings


:copyright: (c) 2017 by Haibo Wang.
"""



import copy
from collections import MutableMapping


class Settings(MutableMapping):
    """
    the Settings looks like a dict structure,but it has
    some useful methods that dict don't have.
    such as fronzen, copy etc.

    """

    def __init__(self):
        self.attributes = {}
        self.freeze = False

    def __contains__(self, name):
        return name in self.attributes

    def __iter__(self):
        return iter(self.attributes)

    def __len__(self):
        return len(self.attributes)


    def __getitem__(self, name):
        if name not in self:
            return None
        return self.attributes[name]

    def get(self,name,default=None):
        return self[name] if self[name] is not None else default

    def __setitem__(self, key, value):
        self.set(key,value)

    def set(self,key,value):
        self._assert_mutablity()
        self.attributes[key] = value

    def __delitem__(self, name):
        self._assert_mutablity()
        del self.attributes[name]

    def _assert_mutablity(self):
        if self.freeze:
            raise TypeError("该类是不可变的")

    def fronzen(self):
        self.freeze = True

    def copy(self):
        return copy.deepcopy(self)

    def fronzencopy(self):
        copy = self.copy()
        copy.fronzen()
        return copy

    def set_variable(self,**kwargs):
        for key in kwargs:
            self.set(key,kwargs[key])


