class Rectangle(object):
    def __init__(self, rect):
        self.rect = rect

    def paint(self, offset, surface, fore_color, back_color):
        import pygame
        rect = pygame.Rect(self.rect.x+offset.x, self.rect.y+offset.y, self.rect.w, self.rect.h)
        
        rect = rect.clip(surface.get_rect())
        subsurf = surface.subsurface(rect)
        # This is MUCH faster than draw.rect
        subsurf.fill(back_color)
        
        pygame.draw.rect(surface, fore_color, rect, 2)
        
    def intersections(self, src, dest):
        # Not implemented.
        return tuple()
