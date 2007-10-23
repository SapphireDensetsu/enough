import pygame

def fill(display, color):
    pass

def rect(surface, color, rect, width=0):
    pass

def line(surface, color, startpos, endpos, width=1):
    pass

def arc(surface, color, Rect, angle_start, angle_stop, width=0):
    pass


def set_mode(size, flags, depth=0):
    return pygame.display.set_mode(size, flags | pygame.DOUBLEBUF | pygame.OPENGL, depth)

class FontFaker(object):
    def __init__(self, name, size):
        self.name = name
        self._size = size

    def render(self, text, antialias, fore_color, back_color=None):
        # todo return a fake surface used later for drawing the font 
        return None

    def size(self, text):
        # todo return the real size
        return self._size*len(text), self._size

def get_font(name, size):
    return FontFaker(name, size)

def draw_font(surface, font_rendered_surface, pos):
    pass
    #surface.blit(font_rendered_surface, *args, **kw)

