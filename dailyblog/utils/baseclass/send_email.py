#encoding:utf8

import email
import time
from email.MIMEText import MIMEText
from email.MIMEMultipart import MIMEMultipart
import smtplib
import os
import ConfigParser
import ast
from . import BaseConfig

class Mail(BaseConfig):

    def __init__(self,obj,path=None):
        super(Mail,self).__init__()
        self.obj, self.path = obj, path
        self._set_server()
        self._set_config()

    def _set_server(self):
        self.email_var = self.settings['EMAIL']
        self.send_server = self.email_var['EMAIL_HOST']
        self.user = self.email_var['EMAIL_HOST_USER']
        self.port = self.email_var['EMAIL_PORT']
        self.password = self.email_var['EMAIL_HOST_PASSWORD']


    def _set_config(self):
        cfg_path = self.path if self.path is not None else os.path.join(os.getcwd(),'config')
        filepath = os.path.join(cfg_path,'sendemail.cfg')
        self.filepath = filepath
        self.cfg = ConfigParser.ConfigParser()
        self.cfg.read(filepath)
        self.to_addrs =ast.literal_eval(self.cfg.get(self.obj,'addrs'))
        self.subject = self.cfg.get(self.obj,'subject')

    def send_email(self,filename=None,msghtml=None,msgtxt=None):
        ms = MIMEMultipart()
        Addrs = [email.utils.formataddr((False,addr)) for addr in self.to_addrs]
        ms['To'] = ','.join(Addrs)
        ms['From'] = self.user
        ms['Subject'] = self.subject
        ms['Date'] = email.utils.formatdate(time.time(),True)
        #ms.attach(MIMEText(self.txt))
        if msghtml:
            ms.attach(MIMEText(msghtml, 'html', 'utf8'))

        if filename:
            attat = MIMEText(file(filename, 'rb').read(), 'base64', 'utf8')
            attat["Content-Type"] = 'application/octet-stream'
            attat['Content-Disposition'] = 'attatcnment;filename="%s" ' % filename
            ms.attach(attat)

        if msgtxt:
            ms.attach(MIMEText(msgtxt, 'plain', 'utf8'))
        try:
            self.smtp = smtplib.SMTP_SSL(self.send_server,self.port)
            #self.smtp.connect(self.send_server)
            self.smtp.login(self.user,self.password)
            self.smtp.sendmail(ms['From'],Addrs,ms.as_string())
            self.smtp.quit()
        except Exception,e:
            print str(e)




if __name__=="__main__":
    S_mail = Mail('daily')
    print os.environ.keys()
    html = """
        <h3> 2017-03-08</h3>
    <table cellpadding="1" cellspacing="0" width="100%" border="1">
        <tr bgcolor="silver">
        <th align=center>id</th>
        <th align=center>title</th>
        <th align=center>salary</th>
        <th align=center>link</th>
        </tr>
        <tr>
            <td align=center>1</td>
            <td align=center>python</td>
            <td align=center>8001</td>
            <td align=center>htm</td>
        </tr>
    </table>


    """
    S_mail.send_email(msghtml=html)




