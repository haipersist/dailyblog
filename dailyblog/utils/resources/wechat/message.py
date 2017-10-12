# -*- coding: utf-8 -*-
__author__ = 'WHB'

#msg types includes:text,image,voice,music,video,link,location etc
MSG_TYPES = {}

def Add_type(msg_type):
    def inner(obj):
        MSG_TYPES[msg_type] = obj
        return obj
    return inner


class WechatMsg(object):
    """
    get common fields:
    ToUserName,equals to wechat server(that is me)
    FromUserName,equals to User
    MsgType,used to get corresponding field later
    """
    def __init__(self,metaMsg):
        self.server = metaMsg.pop('ToUserName')
        self.user = metaMsg.pop('FromUserName')
        self.msgtype = metaMsg.pop('MsgType')


@Add_type('text')
class TextMsg(WechatMsg):
    """
    text msg :
    require:Content
    """
    def __init__(self,metaMsg):
        self.content = metaMsg.pop('Content')
        super(TextMsg,self).__init__(metaMsg)


@Add_type('image')
class ImageMsg(WechatMsg):
    """
    image msg:
    require:
        PicUrl
        MediaId
    """
    def __init__(self,metaMsg):
        self.picurl = metaMsg.pop('PicUrl')
        self.mediaid = metaMsg.pop('MediaId')
        super(ImageMsg,self).__init__(metaMsg)


@Add_type('voice')
class VoiceMsg(WechatMsg):
    """
    voice msg:
    require:
        Format
        MediaId
    """
    def __init__(self,metaMsg):
        self.format = metaMsg.pop('Format')
        self.mediaid = metaMsg.pop('MediaId')
        self.recognition = metaMsg.pop('Recognition')
        super(VoiceMsg,self).__init__(metaMsg)


@Add_type('event')
class EventMsg(WechatMsg):
    """
    Event msg:
    require:
        Format
        MediaId
    """
    def __init__(self,metaMsg):
        self.event = metaMsg.pop('Event')
        super(EventMsg,self).__init__(metaMsg)


@Add_type('link')
class LinkMsg(WechatMsg):
    """
    link msg:
    require:
        Description
        Url
        Title
    """
    def __init__(self,metaMsg):
        self.title = metaMsg.pop('Title')
        self.url = metaMsg.pop('Url')
        self.desc = metaMsg.pop('Description')
        super(LinkMsg,self).__init__(metaMsg)


@Add_type('video')
class VideoMsg(WechatMsg):
    """
    video msg:
    require:
        ThumbMediaId
        MediaId

    """
    def __init__(self,metaMsg):
        self.mediaid = metaMsg.pop('MediaId')
        self.thumbmediaid = metaMsg.pop('ThumbMediaId')
        super(VideoMsg,self).__init__(metaMsg)


@Add_type('shortvideo')
class ShortVideoMsg(WechatMsg):
    """
    shortvideo msg:
    require:
        ThumbMediaId
        MediaId

    """
    def __init__(self,metaMsg):
        self.mediaid = metaMsg.pop('MediaId')
        self.thumbmediaid = metaMsg.pop('ThumbMediaId')
        super(ShortVideoMsg,self).__init__(metaMsg)


@Add_type('music')
class MusicMsg(WechatMsg):
    """
    Music msg:
    require:
        ThumbMediaId
        MediaId

    """
    def __init__(self,metaMsg):
        self.url = metaMsg.pop('MusicUrl')
        self.thumbmediaid = metaMsg.pop('ThumbMediaId')
        self.title = metaMsg.pop('Title')
        super(MusicMsg,self).__init__(metaMsg)


@Add_type('news')
class NewsMsg(WechatMsg):
    """
    News msg:
    require:
        ThumbMediaId
        MediaId

    """
    def __init__(self,metaMsg):
        self.articles = metaMsg.pop('Articles')
        self.picurl = metaMsg.pop('PicUrl')
        self.url = metaMsg.pop('Url')
        self.title = metaMsg.pop('Title')
        super(NewsMsg,self).__init__(metaMsg)
