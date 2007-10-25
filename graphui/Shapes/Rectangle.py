# Copyright (c) 2007 Enough Project.
# See LICENSE for details.

import pygame

from Lib.image import fast_scale

class Rectangle(object):
    def __init__(self, rect):
        self.rect = rect

    def paint(self, offset, surface, fore_color, back_color, use_image=None, image_margin = 2):
        rect = pygame.Rect(self.rect.x+offset.x, self.rect.y+offset.y, self.rect.w, self.rect.h)
        if use_image:
            # image_margin is used because some images have a
            # transparent border of a few pixels to make them blend
            # better
            scaled = fast_scale(use_image, (rect.w+image_margin*2,self.rect.h+image_margin*2), cache_delta=1)
            surface.blit(scaled, (rect.x-image_margin,rect.y-image_margin))
        else:
            if back_color:
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
