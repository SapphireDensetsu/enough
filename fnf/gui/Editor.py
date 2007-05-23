from Lib.Point import Point
from base import App, Widget, Order, mouse_pos

import pygame
import string

class Editor(App):
    def __init__(self, *args, **kw):
        super(Editor, self).__init__(*args, **kw)
        self.register_pygame_event(pygame.KEYUP, self.key_up)
        self.register_pygame_event(pygame.MOUSEBUTTONDOWN, self.mouse_down)
        self.register_pygame_event(pygame.MOUSEBUTTONUP, self.mouse_up)
        self.register_pygame_event(pygame.MOUSEMOTION, self.update_drag)
        #self.register_event('paint', self.update_drag)
        
        self.connecting_widget = None
        self.was_typing = False
        self.drag_widget = None

    def update_drag(self, event):
        if self.drag_widget:
            self.drag_widget.pos = mouse_pos()

    def mouse_down(self, e):
        if not self.hovered_widget:
            return
        self.lock_positions()
        self.connecting_widget = self.hovered_widget
        self.drag_widget = Widget(Point(5,5))
        self.drag_widget.pos = mouse_pos()
        self.drag_widget.speed *= 3
        self.drag_widget.order.ignore = True
        self.add_widget(self.drag_widget)
        self.connect_widgets(self.connecting_widget, self.drag_widget)

    def connect_widgets_permanently(self, w1, w2):
        # todo get rid of this silly func and find another way to tell
        # the difference between real connection and connection of the
        # drag widget
        self.connect_widgets(w1, w2)
        
    def mouse_up(self, e):
        if not self.drag_widget:
            return
        self.disconnect_widgets(self.connecting_widget, self.drag_widget)
        self.remove_widget(self.drag_widget)
        self.drag_widget = None
        self.unlock_positions()
        
        if self.connecting_widget and self.hovered_widget and self.connecting_widget != self.hovered_widget:
            if self.widgets_connected(self.connecting_widget, self.hovered_widget):
                self.disconnect_widgets(self.connecting_widget, self.hovered_widget)
            else:
                self.connect_widgets_permanently(self.connecting_widget, self.hovered_widget)
        self.connecting_widget = None

    def key_up(self, e):
        if e.mod & pygame.KMOD_CTRL:
            if e.key == pygame.K_n:
                w = Widget(Point(15,15))
                if self.widgets:
                    other = random.choice(self.widgets).node
                    # w.node.connect_in(other)
                #w.set_text('moshe')
                w.order.sublevel = self._sublevel
                self.add_widget(w)
        else:
            k = e.key
            if (0 <= k and k < 256):
                k = chr(k)
                if k in string.printable:
                    if not self.hovered_widget:
                        self.printable_key_up(self.hovered_widget, k)

    def printable_key_up(self, widget, ch):
        t = widget.text_lines[0]
        if t is None:
            t = ''
        self.hovered_widget.set_text_line(0, t + ch)
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
    
