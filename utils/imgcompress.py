from __future__ import unicode_literals
#-*- coding:utf-8 -*-
import os
from PIL import Image


class ImageThumb(object):

    def __init__(self,dest_width=1000,dest_height=1000):
        self.dest_width ,self.dest_height = dest_width, dest_height
        self.size = (self.dest_width ,self.dest_height)

    def thumbnail(self,picture):
        img = Image.open(picture)
        f,z = os.path.splitext(picture)
        print f,z
        width,height = img.size
        print width,height
        if width > self.dest_width and height > self.dest_height:
            width_rate = width/self.dest_width
            height_rate = height/self.dest_height
            rate = width_rate if width_rate > height_rate else height_rate
        else:
            rate = 1
        size = (width/rate,height/rate)
        img.thumbnail(size)
        os.remove(picture)
        outfile = picture
        img.save(outfile,'JPEG')
        print outfile
        return outfile




if __name__ == "__main__":
    from optparse import OptionParser

    parser = OptionParser()
    parser.add_option("-p",'--path',dest='path',help='input convert path')

    option,args  = parser.parse_args()
    if option.path is not None:
        path =option.path
        imgcs = ImageThumb()
        for f in os.listdir(path):
            f = path + f
            print imgcs.thumbnail(f)

