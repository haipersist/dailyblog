#!/usr/bin/env python
#-*-coding:utf-8-*-


"""
send_weibo.py:the file provide one simple function,
which can send weibo with pic or without pic


its usage:
weibo = Send_weibo()
weibo.send_weibo('python is wonderful')


Copyright C Haibo wang.2016

"""





import json
import os
#from weibo import APIClient
from config import AuthConfig,CUR_DIR



class WeiboApi():

	def __init__(self):
		#self.filename = os.path.join(CUR_DIR,'token.json')
		self._set_client()

	def _set_client(self):
		self.cfg = AuthConfig()
		self.client = APIClient(app_key=self.cfg.app_key,
								app_secret=self.cfg.app_secret,
								redirect_uri=self.cfg.callback_url)
		

	def _set_token(self):
		#jsonfile = file(self.filename,'r')
		#token = json.load(jsonfile)
		token = {"access_token": "2.00ZClKyCQuqacD21db7b063cxSYBRB",
				 "expires": 1641091420,
				 "expires_in": 1641091420,
				 "uid": "2721409931"}

		self.client.set_access_token(token['access_token'],token['expires_in'])
	
	def send_weibo(self,text):
		self._set_token()
		if not isinstance(text,unicode):
			text = unicode(text,'utf-8')
		self.client.statuses.update.post(status=text)

	def send_pic_weibo(self,text,photo):
		self._set_token()
		pic = file(photo,'rb')
		if not isinstance(text,unicode):
			text = text.encode('utf-8')
		self.client.statuses.upload.post(status=text,pic=pic)

	def get_user_timeline(self,userid):
		self._set_token()
		resp = self.client.statuses.user_timeline.get(userid=userid)
		return resp




if __name__ == "__main__":
	robot = WeiboApi()
	text = u'test. @今日头条'
	robot.send_weibo(text)


