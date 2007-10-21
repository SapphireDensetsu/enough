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
    def __init__(self, child_list):
        self.child_list = child_list
        self.child_list.add_observer(self)

    def size(self):
        return self._do(lambda child, child_pos: None)

    def draw(self, surface, pos):
        def func(child, child_pos):
            child.draw(surface, tuple(a+b for a,b in zip(pos, child_pos)))
        total = self._do(func)
        if self.draw_rect:
            r = pygame.Rect(pos, (total[0]-1, total[1]-1))
            pygame.draw.rect(surface, (40, 40, 150), r, 2)

    def _do(self, func):
        cur = [0, 0]
        max_len = 0
        padding = self.padding if self.draw_rect else 0
        cur[0] += padding
        cur[1] += padding
        for child in self.child_list:
            size = child.size()
            func(child, cur)
            max_len = max(max_len, size[self.direction.oaxis])
            cur[self.direction.axis] += size[self.direction.axis] + padding
        total = [None, None]
        total[self.direction.axis] = cur[self.direction.axis]
        total[self.direction.oaxis] = max_len+padding*2
        return tuple(total)

class VBox(Box):
    direction = Vertical

class HBox(Box):
    direction = Horizontal
