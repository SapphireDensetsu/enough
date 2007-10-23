import pygame
from Widget import Widget

class Stack(Widget):
    def __init__(self):
        Widget.__init__(self)
        self.items = []
    def draw(self, surface, pos):
        self.items[-1].draw(surface, pos)
    def update(self):
        return self.items[-1].update()
    def push(self, widget):
        self.items.append(widget)
        self.keymap.set_next_keymap(widget.keymap)
    def pop(self):
        self.items.pop()