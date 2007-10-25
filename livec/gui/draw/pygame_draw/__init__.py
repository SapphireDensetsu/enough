import pygame
from pygame.draw import *

def fill(display, *args, **kw):
    display.fill(*args, **kw)

    
set_mode = pygame.display.set_mode

_font_cache = {}
def get_font(name, size, is_bold=False, is_underline=False, is_italic=False):
    global _font_cache
    f = _font_cache.get((name, size, is_bold, is_underline, is_italic), None)
    if not f:
        f = pygame.font.Font(name, size)
        f.set_underline(is_underline)
        f.set_bold(is_bold)
        f.set_italic(is_italic)
        _font_cache[(name, size, is_bold, is_underline, is_italic)] = f
    return f


def draw_font(surface, font_rendered_surface, pos):
    surface.blit(font_rendered_surface, pos)

def lock(surface):
    surface.lock()

def unlock(surface):
    surface.unlock()
