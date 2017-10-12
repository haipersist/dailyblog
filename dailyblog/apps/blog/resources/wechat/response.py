#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'WHB'

from .message import WechatMsg
import time
from django.http import HttpResponse


class WechatReply(object):

    """
    :parameter:msg,Wechatmsg
    """
    def __init__(self,metaMsg,**kwargs):
        if 'toUser' not in kwargs :
            kwargs['toUser'] = metaMsg.user
        if 'fromUser' not in kwargs :
            kwargs['fromUser'] = metaMsg.server
        if 'msgtype' not in kwargs :
            kwargs['msgtype'] = metaMsg.msgtype

        kwargs['time'] = int(time.time())
        self.reply = {}
        self.reply.update(kwargs)

    def render(self):
        pass



class TextReply(WechatReply):
    """
    TExtXml
    """
    reply_xml = """
    <xml>
    <ToUserName><![CDATA[%s]]></ToUserName>
    <FromUserName><![CDATA[%s]]></FromUserName>
    <CreateTime>%s</CreateTime>
    <MsgType><![CDATA[text]]></MsgType>
    <Content><![CDATA[%s]]></Content>
    <FuncFlag>0</FuncFlag>
    </xml>
    """

    def __init__(self,metaMsg,content):
        super(TextReply,self).__init__(metaMsg,content=content)

    def render(self):
        #must keep the right order
        para = (self.reply['toUser'],self.reply['fromUser'],
                self.reply['time'],self.reply['content'])
        #response = HttpResponse(self.reply_xml % para)
        response =self.reply_xml % para
        return response


class MusicReply(WechatReply):
    """
    Music Template
    """
    reply_xml = """<xml><ToUserName><![CDATA[%s]]></ToUserName>
     <FromUserName><![CDATA[%s]]></FromUserName>
     <CreateTime>%s</CreateTime>
     <MsgType><![CDATA[music]]></MsgType>
     <Music>
     <Title><![CDATA[%s]]></Title>
     <Description><![CDATA[%s]]></Description>
     <MusicUrl><![CDATA[%s]]></MusicUrl>
     <HQMusicUrl><![CDATA[%s]]></HQMusicUrl>
     </Music>
     <FuncFlag>0</FuncFlag></xml>"""

    def __init__(self,metaMsg,title,desc,musicurl,hqurl):
        super(MusicReply,self).__init__(metaMsg,title=title,desc=desc,musicurl=musicurl,hqurl=hqurl)

    def render(self):
        #must keep the right order
        para = (self.reply['toUser'],self.reply['fromUser'],
                self.reply['time'],self.reply['title'],self.reply['desc'],self.reply['musicurl'],self.reply['hqurl'])
        #response = HttpResponse(self.reply_xml % para)
        response =self.reply_xml % para
        return response



class ArticleReply(WechatReply):
    """
    Article XML
    """
    reply_xml = u"""
    <xml>
    <ToUserName><![CDATA[%s]]></ToUserName>
    <FromUserName><![CDATA[%s]]></FromUserName>
    <CreateTime>%s</CreateTime>
    <MsgType><![CDATA[news]]></MsgType>
    <ArticleCount>%d</ArticleCount>
    <Articles>%s</Articles>
    <FuncFlag>0</FuncFlag>
    </xml>
    """
    Item_xml = u"""
    <item>
    <Title><![CDATA[%s]]></Title>
    <Description><![CDATA[%s]]></Description>
    <PicUrl><![CDATA[%s]]></PicUrl>
    <Url><![CDATA[%s]]></Url>
    </item>"""

    def __init__(self,metaMsg,items):
        self.count = len(items)
        super(ArticleReply,self).__init__(metaMsg,count=self.count,items=items)

    def render(self):
        if self.count >= 10:
            raise AttributeError('the num of articles can not suceed 10')
        Items_tpl = []
        for item in self.reply['items']:
            item_tpl = self.Item_xml % (item['title'],item['desc'],
                                        item['picurl'],item['url'])
            Items_tpl.append(item_tpl)
        Items_tpl = ''.join(Items_tpl)
        para = (self.reply['toUser'],self.reply['fromUser'],
                self.reply['time'],self.reply['count'],Items_tpl)
        response = self.reply_xml % para
        return response





if __name__ == "__main__":
    pass