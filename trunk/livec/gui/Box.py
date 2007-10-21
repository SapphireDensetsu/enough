import pygame
from gui.Widget import Widget

class Direction(object): pass

class Horizontal(Direction):
    axis = 0
    oaxis = 1

class Vertical(Direction):
    axis = 1
    oaxis = 0

class Box(Widget):
    padding = 5
    draw_rect = True
    def __init__(self):
        self.children = []
    def add_child(self, child):
        self.children.append(child)
    def remove_child(self, child):
        self.children.remove(child)
    def draw(self, surface, pos):
        pos = list(pos)
        cur = list(pos)
        max_len = 0
        cur[0] += self.padding
        cur[1] += self.padding
        for child in self.children:
            size = child.draw(surface, cur)
            max_len = max(max_len, size[self.direction.oaxis])
            cur[self.direction.axis] += size[self.direction.axis] + self.padding
        total = [None, None]
        total[self.direction.axis] = cur[self.direction.axis]-pos[self.direction.axis]
        total[self.direction.oaxis] = max_len+self.padding*2
        if self.draw_rect:
            r = pygame.Rect(pos, (total[0]-1, total[1]-1))
            pygame.draw.rect(surface, (40, 40, 150), r, 2)
        return tuple(total)

class VBox(Box):
    direction = Vertical

class HBox(Box):
    direction = Horizontal
