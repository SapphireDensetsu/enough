# Copyright (c) 2007 Enough Project.
# See LICENSE for details.

import pygame

def fill(display, color, rect=None):
    if rect is None:
        display.fill(color)
    else:
        display.fill(color, rect)
        

circle = pygame.draw.circle
ellipse = pygame.draw.ellipse
arc = pygame.draw.arc
rect = pygame.draw.rect

def lines(surface, color, closed, points, width=1, antialias=False):
    if antialias:
        width = 1
        f = pygame.draw.aalines
    else:
        f = pygame.draw.lines
    return f(surface, color, closed, points, width)

def line(surface, color, startpos, endpos, width=1, antialias=False):
    if antialias:
        width = 1
        f = pygame.draw.aaline
    else:
        f = pygame.draw.line
    return f(surface, color, startpos, endpos, width)
    

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


def blit(surface, blit_surface, pos):
    surface.blit(blit_surface, pos)

def save(surface, filename):
    pygame.image.save(surface, filename)
