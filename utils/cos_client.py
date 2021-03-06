#-*- coding:utf-8 -*-


import os
from qcloud_cos import  CosClient,UploadFileRequest,DelFileRequest
from django.conf import settings



class Client(object):

    cos = settings.TECENT_COS
    appid, secret_id, secret_key = cos['APP_ID'], cos['SECRET_ID'], cos['SECRET_KEY']
    region_info = 'tj'
    baseurl = u'http://blog-1251509264.costj.myqcloud.com/'

    def __init__(self):
        self.bucket = u'blog'
        self.client = CosClient(
            self.appid,
            self.secret_id,
            self.secret_key,
            region=self.region_info
        )

    def upload(self,filename):
        sep = os.sep
        #if sep in filename,meaning that the filename is a absolute file path.
        if sep in filename:
            filename = os.path.abspath(filename)
            #the cos path is the name of file.
            cos_path = os.path.basename(filename)
            local_path = filename
        else:
            cos_path = filename
            #get the absolute path of the file,if it is only a filename without any path .
            local_path = os.path.abspath(filename)
        try:
            #sometimes,it needed to be encoded to utf-8
            cos_path, local_path = unicode('/'+cos_path), unicode(local_path)
        except:
            cos_path = '/' + cos_path
        request = UploadFileRequest(self.bucket,cos_path,local_path)
        result = self.client.upload_file(request)
        if result[u'code'] == 0:
            return result['data']['source_url']
        else:
            return {'fail':result['message']}


    def del_file(self,filename):
        if os.path.isdir(filename):
            return None
        request = DelFileRequest(self.bucket,
                                 unicode('/'+filename))
        result = self.client.del_file(request)
        print result
        return result



