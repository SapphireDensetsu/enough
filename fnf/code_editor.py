from gui.Lib.Point import Point
import gui
import code


import pygame
import string

class CodeEditor(gui.Editor):
    def __init__(self, *args, **kw):
        super(CodeEditor, self).__init__(*args, **kw)

    def key_up(self, e):
        if not e.mod & pygame.KMOD_CTRL:
            k = e.key
            if (0 <= k and k < 256):
                k = chr(k)
                if k in string.printable:
                    if not self.hovered_widget:
                        return
                    self.printable_key_up(k)

    def printable_key_up(self, ch):
        t = self.hovered_widget.text
        if t is None:
            t = ''
        self.hovered_widget.set_text(t + ch)

    

import random

def test():
    a = Editor()
    for i in xrange(1):
        w = Widget(Point(20-i,20+i), pos=Point(15*i,23*i), order=Order(i/3))
        a.add_widget(w)
    a.run()

if __name__=='__main__':
    test()
    
