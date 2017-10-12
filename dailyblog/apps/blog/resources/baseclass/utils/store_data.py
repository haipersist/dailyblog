#!/usr/bin/env python
# -*- coding:utf-8 -*-



"""
store_data.py

the data needed sotred is in format:[{},{},{}],we can store them in Mysql ,json or Redis

"""

#from baseclass.database import Database
import json
import os


class Job_Data():

    def __init__(self,store_type='json'):
        self.store_type = store_type

    def store(self,data):
        if self.store_type == 'MySQL':
            self.store_to_mysql(data)
        elif self.store_type == 'json':
            self.store_to_json(data)
        elif self.store_type == 'excel':
            self.store_to_excel(data)
        elif self.store_type == 'redis':
            self.store_to_redis(data)

    def store_to_mysql(self,data):
        self.db = Database('Job')
        self.db.insert_dic_by_list('jobs',data)

    def store_to_json(self,data,filename='job.json'):
        basepath = '/'.join(os.path.abspath(os.path.dirname(__file__)).split('/')[:-1])
        if os.name == 'nt':
            filepath = os.path.join(basepath,'%s'%filename)
            print 'json file is stored in C:\python'
        else:
            filepath = os.path.join('~/',filename)
            print 'json file is stored in ~/ '
        for item in data:
            #print item['title'],item['link']
            json_data = json.dumps(item)
            with file(filepath,'a+') as json_file:
                json_file.write(json_data)
                json_file.write('\n')

    def store_to_excel(self,data,filename='job.xlsx'):
        pass

    def store_to_redis(self,data,keyname='job'):
        pass

    

