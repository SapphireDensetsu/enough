import pygame
from gui.Widget import Widget

class VBox(Widget):
    def __init__(self, get_children_widgets):
        self.get_children_widgets = get_children_widgets
    def draw(self, surface, pos):
        x, y = pos
        cx, cy = pos
        mw = 0
        for child in self.get_children_widgets():
            w, h = child.draw(surface, (cx, cy))
            mw = max(mw, w)
            cy += h
        tw, th = mw, cy-y
        r = pygame.Rect((x, y), (tw-1, th-1))
        pygame.draw.rect(surface, (255, 0, 0), r, 2)
        return (tw, th)
