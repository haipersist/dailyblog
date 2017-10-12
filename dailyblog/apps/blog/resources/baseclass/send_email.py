#!/usr/bin/env python
#encoding:utf8
'''
Author: whb
e-mail:hbnnlong@163.com
Date:2014-04-21
'''

import email
import time
from email.MIMEText import MIMEText
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
import smtplib
import os
import sys
import ConfigParser
import ast
import commands


class SendMail():

    def __init__(self,mail_type,user):
        self.mail_type = mail_type
        self._send_server = 'smtp.163.com'
        PackagePath = commands.getoutput('echo $PackagePath')
        self._cfg_path = '/'.join([PackagePath,'config/sendemail.cfg'])
        self._smtp = smtplib.SMTP(self._send_server)
        self.set_config()
        self.user = user

    def set_config(self):
        self.cfg = ConfigParser.ConfigParser()
        self.cfg.read(self._cfg_path)
        self.to_addrs =ast.literal_eval(self.cfg.get(self.mail_type,'addrs'))
        self.subject = self.cfg.get(self.mail_type,'subject')
        self.txt = self.cfg.get(self.mail_type,'txt')

    def send_email(self,filename=None,msghtml=None,msgtxt=None):
        ms = MIMEMultipart()
        Addrs = [email.utils.formataddr((False,addr)) for addr in self.to_addrs]
        print Addrs
        ms['To'] = ','.join(Addrs)
        ms['From'] = self.user
        ms['Subject'] = self.subject
        ms['Date'] = email.utils.formatdate(time.time(),True)
        #ms.attach(MIMEText(self.txt))
        if msghtml:
            ms.attach(MIMEText(msghtml,'html','utf8'))
   
        if filename:
            attat = MIMEText(file(filename,'rb').read(),'base64','utf8')
            attat["Content-Type"]='application/octet-stream'
            attat['Content-Disposition']='attatcnment;filename="%s" '%filename
            ms.attach(attat)
        
        if msgtxt:
            ms.attach(MIMEText(msgtxt,'plain','utf8'))    
        self._smtp.login(ms['From'],'*******')
        try:
            self._smtp.sendmail(ms['From'],Addrs,ms.as_string())
            self._smtp.quit()
            return
        except Exception,e:
            print str(e)


def test():
    S_mail = SendMail('test','email')
    S_mail.send_email('send_email.py',None,'hello,python')



if __name__=="__main__":

    test()

