#!/usr/bin/env python
# -*- coding: utf-8 -*-


import time
from utils.get_real_ip import get_real_ip
from utils.cache import Cache
from django.core.cache import caches


cache = Cache()

class  LoadTimeMiddleware(object):

    def process_request(self,request):
        self.start = time.time()

    def process_view(self, request, view_func, view_args, view_kwargs):
        online_ips = cache.get('onlines',[])

        if online_ips:
           online_ips = cache.get_many(online_ips).keys()

        self.ip = get_real_ip(request)
        cache.set(self.ip, 'online_ip')

        if self.ip not in online_ips:
            online_ips.append(self.ip)

        cache.set('onlines',online_ips)


    def process_response(self,request,response):
        self.end = time.time()
        load_time = str((self.end - self.start))[:5]
        response.content = response.content.replace('<!!LOAD_TIMES!!>',load_time)
        #response.content = response.content.replace('<!!ONLINE_IPS!!>',str(self.ips))
        return response

