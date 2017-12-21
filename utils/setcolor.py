#-*- coding:utf-8 -*-

"""
setcolor is used to set the color for font.
I have set some common color using it.
such as red,green,blue and so on.



usage:

    print red('hello world')


"""


def setcolor(int_color):
    def inner(msg,bold=False):
        color = '1;{0}'.format(int_color) if bold else str(int_color)
        return '\033[%sm%s\033[0m'%(color,msg)
    return inner




black = setcolor(30)
red = setcolor(31)
green = setcolor(32)
yellow = setcolor(33)
blue = setcolor(34)
cyanine = setcolor(36)
white = setcolor(37)




if __name__ == "__main__":
    print red('s')