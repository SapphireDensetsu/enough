from Lib.Point import Point
from Base import App, Widget, Order, mouse_pos

import pygame
import string

class Editor(App):
    def __init__(self, *args, **kw):
        super(Editor, self).__init__(*args, **kw)
        self.register_pygame_event(pygame.KEYUP, self.key_up)
        self.register_pygame_event(pygame.MOUSEBUTTONDOWN, self.mouse_down)
        self.register_pygame_event(pygame.MOUSEBUTTONUP, self.mouse_up)
        self.register_pygame_event(pygame.MOUSEMOTION, self.mouse_motion)
        self.register_event('paint', self.paint)
        
        self.connecting_widget = None
        self.was_typing = False
        self.drag_widget = None

    def update_drag(self):
        if self.drag_widget:
            self.drag_widget.pos = mouse_pos()

    def paint(self, e):
        self.update_drag()

    def mouse_motion(self, e):
        self.update_drag()
        
        
    def mouse_down(self, e):
        self.lock_positions()
        self.connecting_widget = self.hovered_widget
        self.drag_widget = Widget(Point(5,5))
        self.drag_widget.speed *= 3
        self.drag_widget.order.ignore = True
        self.add_widget(self.drag_widget)
        self.connect_widgets(self.connecting_widget, self.drag_widget)
        
    def mouse_up(self, e):
        self.disconnect_widgets(self.connecting_widget, self.drag_widget)
        self.remove_widget(self.drag_widget)
        self.drag_widget = None
        self.unlock_positions()
        
        if self.connecting_widget and self.hovered_widget and self.connecting_widget != self.hovered_widget:
            if self.widgets_connected(self.connecting_widget, self.hovered_widget):
                self.disconnect_widgets(self.connecting_widget, self.hovered_widget)
            else:
                self.connect_widgets(self.connecting_widget, self.hovered_widget)
        self.connecting_widget = None

    def key_up(self, e):
        if e.mod & pygame.KMOD_CTRL:
            if e.key == pygame.K_n:
                w = Widget(Point(15,15))
                if self.widgets:
                    other = random.choice(self.widgets).node
                    # w.node.connect_in(other)
                #w.set_text('moshe')
                self.add_widget(w)
        else:
            k = e.key
            if (0 <= k and k < 256):
                k = chr(k)
                if k in string.printable:
                    self.printable_key_up(k)

    def printable_key_up(self, ch):
        if not self.hovered_widget:
            return
        t = self.hovered_widget.text
        if t is None:
            t = ''
        self.hovered_widget.set_text(t + ch)
        self.lock_hover()

    

import random

def test():
    a = Editor()
    for i in xrange(1):
        w = Widget(Point(20-i,20+i), pos=Point(15*i,23*i), order=Order(i/3))
        a.add_widget(w)
    a.run()

if __name__=='__main__':
    test()
    
