# prerequisites:
# PyOpenGL - http://pyopengl.sourceforge.net/
# * setuptools http://pypi.python.org/pypi/setuptools#downloads
from OpenGL  import GL

import pygame

def fill(display, color):
    r,g,b = color
    GL.glLoadIdentity()
    GL.glClearColor(r,g,b,0)
    GL.glClear(GL.GL_COLOR_BUFFER_BIT)

def rect(surface, color, rect, width=0):
    GL.glLoadIdentity()
    GL.glColor3f(*color)
    GL.glBegin(GL.GL_LINE_LOOP)
    GL.glVertex2f(*rect.topleft)
    GL.glVertex2f(*rect.topright)
    GL.glVertex2f(*rect.bottomright)
    GL.glVertex2f(*rect.bottomleft)
    GL.glEnd()
    
def line(surface, color, startpos, endpos, width=1):
    GL.glLoadIdentity()
    GL.glColor3f(*color)
    GL.glBegin(GL.GL_LINES)
    GL.glVertex2f(startpos[0], startpos[1])
    GL.glVertex2f(endpos[0], endpos[1])
    GL.glEnd()

def arc(surface, color, Rect, angle_start, angle_stop, width=0):
    # TODO implement
    pass


def set_mode(size, flags, depth=0):
    surface = pygame.display.set_mode(size, flags | pygame.DOUBLEBUF | pygame.OPENGL, depth)

    GL.glShadeModel(GL.GL_SMOOTH) # Enable Smooth Shading
    GL.glClearColor(0.0, 0.0, 0.0, 0.5) # Black Background
    GL.glClearDepth(1.0) # Depth Buffer Setup
    GL.glHint(GL.GL_LINE_SMOOTH_HINT, GL.GL_NICEST) # Set Line Antialiasing
    
    GL.glEnable(GL.GL_TEXTURE_2D)
    GL.glEnable(GL.GL_BLEND) # Enable Blending
    GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA) # Type Of Blending To Use


    GL.glMatrixMode(GL.GL_PROJECTION)
    GL.glLoadIdentity()
    GL.glOrtho(0, size[0], size[1], 0, -1, 1)
    GL.glMatrixMode(GL.GL_MODELVIEW)
    GL.glDisable(GL.GL_DEPTH_TEST)
    return surface

import font

class FontFaker(object):
    def __init__(self, name, size):
        self.name = name
        self._size = size
        self.font = pygame.font.Font(name, size)
        # TODO find a way to colorify the textures even though they were painted white
        self.chars = font.make_chars(self.font)

    def render(self, text, antialias, fore_color, back_color=None):
        # todo return a fake surface used later for drawing the font
        return self, text, fore_color, back_color

    def size(self, text):
        return self.font.size(text)

_font_cache = {}
def get_font(name, size):
    global _font_cache
    if (name,size) in _font_cache:
        return _font_cache[(name,size)]

    f = FontFaker(name,size)
    _font_cache[(name,size)] = f
    return f

def draw_font(surface, fakefont_surface, pos):
    fakefont, text, fore_color, back_color = fakefont_surface # is not really a surface
    font.draw_chars(text, fakefont.chars, fore_color, pos)

