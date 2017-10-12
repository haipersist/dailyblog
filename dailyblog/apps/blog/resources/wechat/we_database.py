__author__ = 'BJHaibo'
# -*-coding:utf-8 -*-
import MySQLdb


class Database():

    config={
                  'local':{
                        'host':'127.0.0.1',
                        'user':'root',
                        'db':'app_dailyblog',
                        'passwd':'320623',
                        'charset':'utf8'},
                  }

    def __init__(self,dbname):
        self._connect(dbname)
        self.dbname = dbname

    def _connect(self,dbname):
        tar = self.config[dbname]
        self.con = MySQLdb.connect(host=tar['host'],
                                   user=tar['user'],
                                   port=tar['port'],
                                   passwd=tar['passwd'],
                                   charset=tar['charset'],
                                   db=tar['db'])
        self.con.ping(True)
        self.cursor = self.con.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        # self.cursor.execute('SET NAMES utf8')

    def query_by_field(self,table, field):
        #this method only deal with one key
        """
        key,value = kwargs.items()[0][0], kwargs.items()[0][1]
        if isinstance(value, int):
            sql = 'select * from %s where %s=%d ' % (table, key, value)
        elif isinstance(value, basestring):
            sql = 'select * from %s where %s=%s ' % (table, key, value)
        else:
            return None
        """
        sql = 'select * from %s where id=%d' % (table,int(field))
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def  get_all_titles(self,table):
        sql = 'select id,title from %s ORDER BY id DESC ' % table
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def query_dic(self,sql,where=None,select=None):
        if where:
            sql="%s where %s" % (sql,where)
        if select:
            sql="%s %s" % (sql,select)
        #print sql
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def insert_by_dic(self,table,data):
        keys = data.keys()
        values = []
        keystr = ','.join('`' + x + '`' for x in keys)
        for key in keys:
            values.append(data[key])
        valstr = ','.join( "'" + x + "'" if isinstance(x,unicode) \
                           else "'" + str(x).decode('utf8') +"'" for x in values )
        sql = "INSERT INTO  %s (%s) VALUES (%s) " % (table,keystr,valstr)
        self.cursor.execute(sql)
        self.con.commit()
        self.con.close()

    def insert_list_dic(self,data,table):
        for item in data:
            try:
                self.insert_by_dic(table, item)
            except MySQLdb.OperationalError:
                self._connect(self.dbname)
                self.insert_by_dic(table, item)
                continue
            except MySQLdb.IntegrityError,e:
                print str(e)
                continue
