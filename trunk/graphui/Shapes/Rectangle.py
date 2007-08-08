import pygame

class Rectangle(object):
    def __init__(self, rect):
        self.rect = rect

    def paint(self, offset, surface, fore_color, back_color):
        rect = pygame.Rect(self.rect.x+offset.x, self.rect.y+offset.y, self.rect.w, self.rect.h)
        if back_color:
            # TODO there is still some bug here that can cause:
            # "subsurface rectangle outside surface area"
            rect = rect.clip(surface.get_rect())
            if rect.width > 0 and rect.height > 0:
                subsurf = surface.subsurface(rect)
                # This is MUCH faster than draw.rect
                subsurf.fill(back_color)

        if fore_color:
            pygame.draw.rect(surface, fore_color, rect, 2)
        
    def intersections(self, src, dest):
        # Not implemented.
        return tuple()
