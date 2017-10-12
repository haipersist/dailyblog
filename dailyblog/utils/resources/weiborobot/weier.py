#!/usr/bin/env python
#encoding:utf8


import datetime
import random

from weiboapi import WeiboApi
from blog.resources.baiduapi.logion import get_logion
from blog.resources.baiduapi.api import LifeApi, ToolApi

class Robot():
	
	def __init__(self):
		self.now = datetime.datetime.today().strftime("%Y-%m-%d %H:%M")
		self.weibo_robot = WeiboApi()
		self.blog = 'http:dailyblog.applinzi.com'

	def ontime_reminder(self):
		text = "现在是北京时间：%s，我亲爱的朋友们，不要熬夜啦，赶紧睡觉。祝你们新的一天一切顺利，Good Day！Behind you forever!。爱你们！—海波" % self.now
		self.weibo_robot.send_weibo(text)
		
	def send_joke(self):
		text = u'(程序自动发送，每日开心一笑）' + get_joke_text()
		self.weibo_robot.send_weibo(text)

	def send_weather(self):
		weather = get_weathe_info()
		self.weibo_robot.send_weibo(weather)

	def send_logion(self):
		try:
			logion = get_logion()
		except:
			logion = random.choice([u'与人为善，铭记给予是一种快乐！',u'没有人能随随便便成功',u'钱不是衡量一个人是否成功的标准，如果每天都过得开心就是成功！'])
		self.weibo_robot.send_weibo(logion)

	def get_timeline(self,userid=2721409931):
		return self.weibo_robot.get_user_timeline(userid)
	
	def send_historyofToday(self):
		api = LifeApi()
		text =  api.HistoryofToday()+ u'(欢迎访问我的网站：%s)' % self.blog
		print text
		self.weibo_robot.send_weibo(text)

if __name__ == "__main__":
	robot = Robot()
	for r in robot.get_timeline().statuses:
		print r.text

