class Rectangle(object):
    def __init__(self, rect):
        self.rect = rect

    def paint(self, offset, surface, fore_color, back_color):
        import pygame
        rect = self.rect.x+offset.x, self.rect.y+offset.y, self.rect.w, self.rect.h
        pygame.draw.rect(surface, back_color, rect, 0)
        # otherwise we get a pygame error for using a width that's larger than the elipse radius
        pygame.draw.rect(surface, fore_color, rect, 2)
        
    def intersections(self, src, dest):
        # Not implemented.
        return tuple()
