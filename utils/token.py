#!/usr/bin/env python
# -*- coding: utf-8 -*-

from itsdangerous import URLSafeTimedSerializer as utsr
import base64
import re

class Token():

    def __init__(self,security_key):
        self.security_key = security_key
        self.salt = base64.encodestring(security_key)

    def generate_validate_token(self,username):
        serializer = utsr(self.security_key)
        return serializer.dumps(username,self.salt)

    def confirm_validate_token(self,token,expiration=3600):
        serializer = utsr(self.security_key)
        return serializer.loads(token,
                          salt=self.salt,
                          max_age=expiration)



if __name__ == "__main__":
    SECRET_KEY = 'gna^*4u41q+qu1mi1rnb&rsv2--o&3f)8yu997ty!nqoq@k4(7'
    confir_token = Token(SECRET_KEY)
    token = confir_token.generate_validate_token('hbnn')
    print confir_token.confirm_validate_token(token)

