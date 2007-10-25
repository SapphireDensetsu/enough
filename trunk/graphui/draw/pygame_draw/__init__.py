# Copyright (c) 2007 Enough Project.
# See LICENSE for details.

import pygame
from pygame.draw import *

def fill(display, *args, **kw):
    display.fill(*args, **kw)

    
set_mode = pygame.display.set_mode

_font_cache = {}
def get_font(name, size):
    global _font_cache
    f = _font_cache.get((name,size), None)
    if not f:
        try:
            f = pygame.font.Font(name, size)
        except IOError:
            print 'Error loading font', name, size
            raise
        _font_cache[(name,size)] = f
    return f


def draw_font(surface, font_rendered_surface, pos):
    surface.blit(font_rendered_surface, pos)

def lock(surface):
    surface.lock()

def unlock(surface):
    surface.unlock()

def blit(surface, blit_surface, pos):
    surface.blit(blit_surface, pos)
