import pygame
from gui.Widget import Widget

class Direction(object): pass

class Horizontal(Direction): axis = 0
class Vertical(Direction): axis = 1

class Box(Widget):
    padding = 5
    def __init__(self, get_children_widgets):
        self.get_children_widgets = get_children_widgets
    def draw(self, surface, pos):
        pos = list(pos)
        cur = list(pos)
        max_len = 0
        cur[0] += self.padding
        cur[1] += self.padding
        for child in self.get_children_widgets():
            size = child.draw(surface, cur)
            max_len = max(max_len, size[self.direction.axis^1])
            cur[self.direction.axis] += size[self.direction.axis] + self.padding
        total = [None, None]
        total[self.direction.axis] = cur[self.direction.axis]-pos[self.direction.axis]
        total[self.direction.axis^1] = max_len+self.padding*2
        r = pygame.Rect(pos, (total[0]-1, total[1]-1))
        pygame.draw.rect(surface, (255, 0, 0), r, 2)
        return tuple(total)

class VBox(Box):
    direction = Vertical

class HBox(Box):
    direction = Horizontal
