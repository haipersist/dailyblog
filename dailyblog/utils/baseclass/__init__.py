#-coding:utf-8 -*-

from .config.set_variable import set_baseclass_var


class BaseConfig(object):

    def __init__(self):
        self.settings = set_baseclass_var()


