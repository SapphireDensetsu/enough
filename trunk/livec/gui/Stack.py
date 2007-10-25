# Copyright (c) 2007 Enough Project.
# See LICENSE for details.

import pygame
from Widget import Widget

class Stack(Widget):
    def __init__(self):
        Widget.__init__(self)
        self.items = []
    def draw(self, surface, pos):
        self.top().draw(surface, pos)
    def update(self):
        self.top().update()
        self.size = self.top().size
    def push(self, widget):
        self.items.append(widget)
        self._update_state()
    def remove(self, item):
        self.items.remove(item)
        self._update_state()
    def pop(self):
        self.items.pop()
        self._update_state()
    def top(self):
        return self.items[-1]
    def _update_state(self):
        if self.items:
            top = self.top()
            self.selectable = top.selectable
            self.keymap.set_next_keymap(top.keymap)
        else:
            self.selectable = False
            self.keymap.set_next_keymap(None)
