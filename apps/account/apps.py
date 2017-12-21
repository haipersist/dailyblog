from __future__ import unicode_literals

from django.apps import AppConfig
from .views import test_sig
from django.contrib.auth.signals import user_logged_in




class AccountConfig(AppConfig):
    name = 'apps.account'



    def ready(self):
	    user_logged_in.connect(test_sig,sender=user_logged_in)




default_app_config = 'apps.account.apps.AccountConfig'
	
