#!/usr/bin/python
# -*-coding:utf-8 -*-
import MySQLdb

class Database():
    
    config={

                   'Job': {
                        'host': '127.0.0.1',
                        'user': 'root',
                        'passwd': '320623',
                        'db': 'Job',
                        'charset': 'utf8'},
                  'local':{
                        'host':'127.0.0.1',
                        'user':'root',
                        'db':'***',
                        'passwd':'********',
                        'charset':'utf8'}
                 }
    
    def __init__(self,dbname):
        self._connect(dbname)
    
    def _connect(self,dbname):
        tar = self.config[dbname]
        self.con = MySQLdb.connect(tar['host'],tar['user'],tar['passwd'],tar['db'],charset=tar['charset'])
        self.cursor = self.con.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        self.cursor.execute('SET NAMES utf8')
    
    def query_dic(self,sql,where=None,select=None):
        if where:
            sql = "%s where %s" % (sql,where)
        if select:
            sql = "%s %s" % (sql,select)
        #print sql
        self.cursor.execute(sql)
        return self.cursor.fetchall()
     
    
    def sql_exec(self, sql):
        self.cursor.execute(sql)
        self.conn.commit()

        
    def create_table(self,tablename,columns):
        sql = 'create table `%s`(%s)'%(tablename,columns)
        self.sql_exec(sql)
        
    def insert_by_dic(self,table,data):
        keys=data.keys()
        values=[]
        keystr = ','.join('`' + x + '`' for x in keys)
        for key in keys:
            values.append(data[key])
        valstr = ','.join( "'" + x + "'" if isinstance(x,unicode) \
                           else "'" + str(x).decode('utf8') +"'" for x in values )   
        sql="INSERT INTO  %s (%s) VALUES (%s) " % (table,keystr,valstr)
        self.cursor.execute(sql)
        self.con.commit()
    
        
    def insert_dic_by_list(self, table, tar_data):
        for data in tar_data:
            try:
                self.insert_by_dic(table, data)        
            except Exception,e:
                    print str(e),data
                    continue
                
    def update_(self,table,key,value,ref_key,ref_value):
        sql = 'update %s set %s="%s" where %s="%s"'\
              %(table,key,value,ref_key,ref_value)
        #print sql
        self.sql_exec(sql)
        
    def update_by_dic(self,table,ref_key,ref_value,data):
        keys = data.keys()
        values=[]
        keystr = ['`' + x + '`' for x in keys]
        for key in keys:
            values.append(data[key])
        valstr = [ "'" + x + "'" if isinstance(x,unicode) \
                           else "'" + str(x).decode('utf8') +"'" for x in values]
        obj = ','.join(str(keystr[index])+"=%s"%valstr[index] \
                       for index in range(0,len(keys)))
        sql = 'UPDATE %s set %s where %s="%s"'%(table,obj,ref_key,ref_value)
        self.cursor.execute(sql)
        self.con.commit()


    def update_list_dic(self,table,ref_key,data):
        for d in data:
            try:
                ref_value=str(d[ref_key])
                self.update_by_dic(table,ref_key,ref_value,d)
            except Exception,e:
                print str(e),d
                continue

    def load_file_to_db(self, table, file_name):
        sql_load = "LOAD DATA LOCAL INFILE '%s' INTO TABLE %s \
                FIELDS TERMINATED BY ',' \
                ENCLOSED BY '' LINES TERMINATED BY '\n' " % ( 
            file_name, table)
        self.cursor.execute(sql_load)
        self.conn.commit()




