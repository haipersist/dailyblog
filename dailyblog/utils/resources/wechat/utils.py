#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'WHB'

#from lxml import etree
import xml.etree.ElementTree as ET
#from mako.template import Template
#from mako.lookup import TemplateLookup



'''
directory=os.path.join(os.path.dirname(__file__),'template/')


def data2html(data,tplname):
    lookup = TemplateLookup(directories=[directory],
                          input_encoding='utf8',
                          output_encoding='utf8',
                          encoding_errors='replace')
    tar = lookup.get_template(tplname)
    return tar.render(data_list=data)


class Send_Mail():
    """
    send mail to myself,modify me if some error happen
    :parameter message,title,
    """
    def __init__(self,toUser):
        self.mail = EmailMessage()
        self.mail.to = toUser
        self.myemail = ''
        self.pwd = ''
        self.mail.smtp = ('smtp.vampire.com', 25, self.myemail, self.pwd, False)

    def send(self,title,msg):
        self.mail.subject = title
        self.mail.html = data2html(msg,'tplname')
        self.mail.send()

'''

def parse_xml(metadata):
    """
    :param metadata:
    :return one dict :
    """
    data = {}
    root = ET.fromstring(metadata)
    '''
    ToUserName = xml_recv.find("ToUserName").text
    FromUserName = xml_recv.find("FromUserName").text
    MsgType = xml_recv.find("MsgType").text
    Content = xml_recv.find('Content').text
    return {'ToUserName':ToUserName,'FromUserName':FromUserName,
            'MsgType':MsgType,'Content':Content}
    '''
    for child in root:
        data.setdefault(child.tag,child.text)
    data.pop('CreateTime')
    return data


if __name__ == "__main__":
    xml = u"""
    <xml>
    <ToUserName><![CDATA[d]]></ToUserName>
    <FromUserName><![CDATA[f]]></FromUserName>
    <CreateTime>13</CreateTime>
    <MsgType><![CDATA[text]]></MsgType>
    <Content><![CDATA[rhh]]></Content>
    </xml>
    """
    print parse_xml(xml)
