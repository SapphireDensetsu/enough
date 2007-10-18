import pygame
from Widget import Widget

class Stack(Widget):
    def __init__(self):
        self.items = []
    def draw(self, surface, pos):
        return self.items[-1].draw(surface, pos)
    def push(self, widget):
        self.items.append(widget)
    def pop(self):
        self.items.pop()
