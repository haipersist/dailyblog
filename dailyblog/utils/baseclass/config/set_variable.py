from __future__ import unicode_literals
#-*-coding:utf-8 -*-



from ...var_setting import Settings
from .dbsetting import DATABASES
from .envvar import EMAIL




def set_baseclass_var():

    setting = Settings()
    setting.set_variable(mysql=DATABASES['mysql'],
                         redis=DATABASES['redis'],
                         email=EMAIL
                         )
    return setting








