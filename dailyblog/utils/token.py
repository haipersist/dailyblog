# -*- coding: utf-8 -*-
"""
 Considerating security,I write one class to provide the security
 of my website.

 Token is very import in the security field

 Encrypt:base64 ,but first use itsdangerous to serialize,idea from Flask.

 Decrypt:has a expire time, if exceeds the time,it's invalid.



 :copyright: (c) 2016 by Haibo Wang.
"""



from itsdangerous import URLSafeTimedSerializer as utsr
import base64
from dailyblog.settings import SECRET_KEY





class Token():

    def __init__(self,security_key=SECRET_KEY):
        self.security_key = security_key
        self.salt = base64.encodestring(security_key)

    def generate_validate_token(self,username):
        serializer = utsr(self.security_key)
        return serializer.dumps(username,self.salt)

    def confirm_validate_token(self,token,expiration=3600*24):
        serializer = utsr(self.security_key)
        return serializer.loads(token,
                          salt=self.salt,
                          max_age=expiration)



if __name__ == "__main__":
    SECRET_KEY = 'gna^*4u41q+qu1mi1rnb&rsv2--o&3f)8yu997ty!nqoq@k4(7'
    confir_token = Token()
    token = confir_token.generate_validate_token('393993705@qq.com')
    print confir_token.confirm_validate_token(token)

