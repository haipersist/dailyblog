#!/usr/bin/env python
#-*- coding:utf-8 -*-
__author__='whb'

def setcolor(color):
    def inner(msg,bold=False):
        color = '1;%d'%color if bold else str(color)
        return '\033[%sm%s\033[0m'%(color,msg)
    return inner


black = setcolor(30)
red = setcolor(31)
green = setcolor(32)
yellow = setcolor(33)
blue = setcolor(34)
cyanine = setcolor(36)
white = setcolor(37)

