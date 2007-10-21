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
    frame_color = (30, 30, 80)
    is_centered = False

    def has_frame(self):
        return self.frame_color is not None
    
    def __init__(self, child_list):
        self.child_list = child_list
        self.child_list.add_observer(self)

    def size(self):
        def ignore_child(child, child_pos, child_size, padding):
            pass
        return self._do(ignore_child)

    def draw(self, surface, pos):
        self_size = self.size()
        def draw_child(child, child_pos, child_size, padding):
            abs_pos = [a+b for a,b in zip(pos, child_pos)]
            if self.is_centered:
                offset = (self_size[self.direction.oaxis] -
                          child_size[self.direction.oaxis]) / 2
            else:
                offset = padding
            abs_pos[self.direction.oaxis] += offset
            child.draw(surface, abs_pos)
        total = self._do(draw_child)
        if self.has_frame():
            r = pygame.Rect(pos, (total[0]-1, total[1]-1))
            pygame.draw.rect(surface, self.frame_color, r, 2)

    def _do(self, func):
        cur = [0, 0]
        max_len = 0
        cur[self.direction.axis] = self.padding
        for child in self.child_list:
            size = child.size()
            func(child, cur, size, self.padding)
            max_len = max(max_len, size[self.direction.oaxis])
            cur[self.direction.axis] += size[self.direction.axis]+self.padding
        total = [None, None]
        total[self.direction.axis] = cur[self.direction.axis]
        total[self.direction.oaxis] = max_len+self.padding*2
        return tuple(total)

class VBox(Box):
    direction = Vertical

class HBox(Box):
    direction = Horizontal
