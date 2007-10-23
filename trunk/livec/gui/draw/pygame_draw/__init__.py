import pygame
from pygame.draw import *

def fill(display, *args, **kw):
    display.fill(*args, **kw)

    
set_mode = pygame.display.set_mode

def get_font(name, size):
    return pygame.font.Font(name, size)

def draw_font(surface, font_rendered_surface, pos):
    surface.blit(font_rendered_surface, pos)
