#!/usr/bin/env python
# -*- coding: utf-8 -*-


import time

class  LoadTimeMiddware(object):

    def process_request(self,request):
        self.start = time.time()

    def process_view(self, request, view_func, view_args, view_kwargs):
        pass

    def process_response(self,request,response):
        self.end = time.time()
        load_time = str((self.end - self.start))[:5]
        response.content = response.content.replace('<!!LOAD_TIMES!!>',load_time)
        return response

