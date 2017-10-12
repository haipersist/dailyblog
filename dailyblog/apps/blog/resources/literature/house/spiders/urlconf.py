 # -*- coding: utf-8 -*-


class Jj(object):

    def __init__(self):
        self.base_url = "http://www.jj59.com"



class JiJinpin(Jj):

    def __init__(self):
        super(JiJinpin,self).__init__()
        self.request_url = self.base_url + '/jingpinwenzhang/'
        self.list = 68



class JiSanwen(Jj):

    def __init__(self):
        super(JiSanwen,self).__init__()
        self.request_url = self.base_url + '/sanwen/youmeisanwen/'
        self.list = 132


class JiMingren(Jj):

    def __init__(self):
        super(JiMingren,self).__init__()
        self.request_url = self.base_url + '/sanwen/mingjiasanwen/'
        self.list = 133



class meilu(object):

    def __init__(self):
        self.base_url = "http://www.vipyl.com"


class MlYulu(meilu):

    def __init__(self):
        super(MlYulu,self).__init__()
        self.request_url = self.base_url + "/article/140/"


class MlJingpin(meilu):

    def __init__(self):
        super(MlJingpin,self).__init__()
        self.request_url = self.base_url + "/article/33/"


class Mw(object):

    def __init__(self):
        self.base_url = "http://www.lookmw.cn"

class MwYulu(Mw):

    def __init__(self):
        super(MwYulu,self).__init__()
        self.request_url = self.base_url +'/jingdianyulu/'
        self.list = 63450


class Wenzhangba(object):
     def __init__(self):
        self.base_url = "http://www.wenzhangba.com"


class WzbWenzhai(Wenzhangba):

     def __init__(self):
        super(WzbWenzhai,self).__init__()
        self.request_url = self.base_url +'/source/'