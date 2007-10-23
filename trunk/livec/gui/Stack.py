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
        self.keymap.set_next_keymap(widget.keymap)
    def pop(self):
        self.items.pop()
    def top(self):
        return self.items[-1]
