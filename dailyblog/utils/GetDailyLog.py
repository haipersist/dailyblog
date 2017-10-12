#-*- coding:utf-8 -*-


"""
    API参数介绍：
    SAE日志API的URL请求格式为： GET /log/(string: service)/(string: date)/(string: ident).log?(string: fop)

    参数列表中：

    date表示日志的日期，格式为yyyy-MM-dd

    service为SAE提供的各项服务，包括http，taskqueue（任务队列），cron（定时任务），mail（邮件），rdc（关系型数据库集群），storage（存储），push（推送）以及fetchurl（URL抓取），相信熟悉SAE的开发不会对此感到陌生。

    ident表示相应服务下的日志类型，包括access（访问），error（错误），alert（警报），debug（调试），warning（警告）与 notice（通知）。

    service与ident的对应关系见下表（摘自SAE日志API文档）：

    service ident
    http access、error、alert、debug、warning、notice
    taskqueue error
    cron error
    mail access、error
    rdc error、warning
    storage access
    push access
    fetchurl access
    fop（似乎是flow operation的简称），为流式操作参数，支持head，tail，grep等linux下常用的shell命令；并且支持管道，操作之间用竖线分隔

    fop操作指令列表（摘自SAE日志API文档）：

    head/OFFSET/LIMIT：获取日志开头行，OFFSET是起始行号，LIMIT是获取的最大行数。
    tail/OFFSET/LIMIT：获取日志末尾行，OFFSET是起始行号（最后一行行号为1），LIMIT是获取的最大行数。
    grep/PATTERN：关键字匹配，参数为关键字，支持部分正则，遵循lua正则语法，如 yq2[^6]+$ 。
    fields/SEPERATOR/COL1/COL2/...：取部分列。SEPERATOR指定列与列的分隔符，COL1等是要取的列的序号，从1开始。
    uniq/SEPERATOR/COL1/COL2/...：去除相邻重复的行，可以指定通过哪些列来排重，若无参数则比较整行，参数同fields指令。 日志API使用方法：
"""


import requests
from datetime import date,timedelta
from authhandler import SaeApibusAuth



class DailyLog():

    service = {
        'http':['access','error','alert','debug','warning','notice'],
        'taskqueue':['error'],
        'cron':['error'],
        'mail':['access、error'],
        'rdc':['error','warning'],
        'storage':['access'],
        'push':['access'],
        'fetchurl':['access']
    }

    def __init__(self,day=None):
        self.day = date.today().strftime("%Y-%m-%d") if day is None else day
        self.accesskey,self.secretkey =  '5n530w1n50', 'm5k5lyjx4hh30k3zyxi4ymyz4xlkmmhkhxxkkzwy'
        self.auth = SaeApibusAuth(self.accesskey,self.secretkey)
        self.saeurl = 'http://g.sae.sina.com.cn/'

    def getdailylog(self,service='http',indent='access',fop=None):
        fop = fop if fop is not None else ''
        content = requests.get('%s/log/%s/%s/2-%s.log?%s' % (self.saeurl,service,self.day,indent,fop),
                               auth=self.auth).content
        return content

    def store_daily_ips(self):
        fop = 'fields/ /2/5'
        self.logfile = '/tmp/%s-dailyblog-visitips.log' % self.day
        content = self.getdailylog(fop=fop)
        with file(self.logfile,'w') as f:
            f.write(content)

    def up2online(self):
        with file(self.logfile,'r') as f:
            for line in f.readlines():
                line = line.split(' ')
                ip,timestamp = line[0],line[1]
                timestamp = timestamp.replace('[','').replace('\n','').split(':')[1:]
                visit_time = "%s %s" % (self.day,':'.join(timestamp))
                fields = {'ip':ip,'visit_time':visit_time}
                print fields,'fields'
                try:
                    r = requests.post('http://dailyblog.applinzi.com/api/visitips/',
                                  data=fields,
                                  auth=('haibo_persist', 'NANAnana320'))
                except Exception,e:
                    print str(e)
                    continue



if __name__ == "__main__":
    import sys
    day = None if len(sys.argv)==1 else sys.argv[1]
    log = DailyLog(day=day)
    log.store_daily_ips()
    log.up2online()








