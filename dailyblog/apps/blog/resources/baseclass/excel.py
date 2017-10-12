# -*- coding: UTF-8 -*-
#!/usr/bin/env python
__author__ = 'whb'

import xlwt
import xlrd
from xlutils.copy import copy
import time
import shutil
import os,sys
import commands


class Excel(object):

    def __init__(self,filename):
        # get the full name of excel
        self.xlsname ='.'.join([filename,'xls'])


    def move(self,dest):
        shutil.move(self.xlsname,dest)

    def sync(self,dest):
        # compared to move method,it can modify the existence file
        os.system('rsync -av %s %s'%(self.xlsname,dest))

    def _connect_excel(self,read_only=True,create_new=None):
        '''
        if the target file dose not exist,then create file named self.xlsname
        :param create:
        :return:workbook
        '''
        try:
            return copy(xlrd.open_workbook(self.xlsname))
        except Exception,e:
            if create_new:
                print 'create new'
                obj = xlwt.Workbook(encoding='utf8')
                obj.add_sheet('sample')
                obj.save(self.xlsname)
                return copy(xlrd.open_workbook(self.xlsname))
            else:
                print create_new,'fuck'
                sys.exit(0)


class RExcel(Excel):

    def __init__(self,filename,data_struct):
        super(RExcel,self).__init__(filename)
        self.obj = self._connect_excel()
        self.data_struct = data_struct

    def get_sheet(self,sheetname = None,sheetid = None):
        if sheetname:
            sheet = self.obj.sheet_by_name(sheetname)
        elif sheetid:
            sheet = self.obj.sheet_by_index(sheetid)
        else:
            print 'pls input sheetname or sheeetid'
            sys.exit(0)
        return sheet

    #data_struct is according to the target excel file {'colname':colnumber}
    def read_one_sheet(self,sheetname=None,sheetid=None):
        self.sheet = self.get_sheet(sheetname,sheetid)
        for row in  range(1,self.sheet.nrows):
            element = {}
            for key in self.data_struct.keys():
                element[key] = self.sheet.cell(row,self.data_struct[key]).value
            yield element

    # read all data of all sheets in target file
    def read_all(self):
        for s in self.obj.sheets():
            for row in range(1,s.nrows):
                values = []
                for c in range(s.ncols):
                    values.append(s.cell(row,c).value)
                print ','.join(values)


class WExcel(Excel):

    def __init__(self,filename,data_struct):
        super(WExcel,self).__init__(filename)
        self.wobj = self._connect_excel(create_new=True)
        self.data_struct = data_struct

    def style(self,**fontargs):
        al = xlwt.Alignment()
        al.horz = xlwt.Alignment.HORZ_CENTER
        al.vert = xlwt.Alignment.VERT_CENTER
        style=xlwt.XFStyle()
        style.alignment=al
        font=xlwt.Font()
        font.name='SimSun'
        font.height=220
        if fontargs:
            for key in fontargs:
                if hasattr(font,key):
                    setattr(font,key,fontargs[key])
        style.font=font
        return self.style


    def _add_sheet(self,sheetname):
        for sh in sheetname:
            self.wobj.add_sheet(sh)
        #self.wobj.save(self.xlsname)


    def write_title(self,sheetid):
        sheet =self.wobj.get_sheet(sheetid)
        al = xlwt.Alignment()
        al.horz = xlwt.Alignment.HORZ_CENTER
        al.vert = xlwt.Alignment.VERT_CENTER
        style = xlwt.XFStyle()
        style.alignment = al
        font = xlwt.Font()
        font.name = 'SimSun'
        font.height = 330
        font.colour_index = 33
        borders = xlwt.Borders()
        borders.left = xlwt.Borders.THICK
        borders.right = xlwt.Borders.THICK
        borders.top = xlwt.Borders.THICK
        borders.bottom = xlwt.Borders.THICK
        style.borders = borders
        style.font = font
        for key in self.data_struct:
            col = int(self.data_struct[key])
            sheet.write(0,col,key,style)

    def write(self,sheetid,data,row):
        sheet = self.wobj.get_sheet(sheetid)
        if isinstance(data,dict):
            for key in item.keys():
                sheet.write(row,int(self.data_struct[key]),item[key])
                row += 1
        elif isinstance(data,tuple and list):
            data = [item for item in data if item]
            for item in data:
                for key in item.keys():
                    print key
                    sheet.write(row,int(self.data_struct[key]),item[key])
                row += 1
        else:
            return

    def save(self):
       self.wobj.save(self.xlsname)


def test():
    data_struct = {u'姓名':0,u'年龄':1}
    #e =Excel('test')
    q = WExcel('tess',data_struct)
    q._add_sheet(['ss','sg'])
    #q.write(data_struct)
    q.write_title(2)
    q.write(1,[{u'年龄':25,u'姓名':u'海波'}],1)
    q.save()
    q.move('e:\\find_job')




if __name__=="__main__":
    test()
    print os.path.abspath('test.xls')




