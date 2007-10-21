import pygame
from Widget import Widget

class Stack(Widget):
    def __init__(self):
        self.items = []
    def draw(self, surface, pos):
        self.items[-1].draw(surface, pos)
    def size(self):
        return self.items[-1].size()
    def push(self, widget):
        self.items.append(widget)
    def pop(self):
        self.items.pop()
