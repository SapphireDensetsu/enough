# Copyright (c) 2007 Enough Project.
# See LICENSE for details.

# prerequisites:
# PyOpenGL - http://pyopengl.sourceforge.net/
# * setuptools http://pypi.python.org/pypi/setuptools#downloads
from OpenGL  import GL

import OpenGL.error
OpenGL.error.ErrorChecker.registerChecker(lambda : None)

import pygame

def fill(display, color):
    r,g,b = color
    GL.glLoadIdentity()
    GL.glClearColor(r,g,b,0)
    GL.glClear(GL.GL_COLOR_BUFFER_BIT)

def rect(surface, color, rect, width=1):
    GL.glLoadIdentity()
    GL.glColor3f(*color)
    GL.glLineWidth(max(width,1))
    GL.glBegin(GL.GL_LINE_LOOP)
    GL.glVertex2f(*rect.topleft)
    GL.glVertex2f(*rect.topright)
    GL.glVertex2f(*rect.bottomright)
    GL.glVertex2f(*rect.bottomleft)
    GL.glEnd()
    
def line(surface, color, startpos, endpos, width=0):
    GL.glLoadIdentity()
    GL.glLineWidth(max(width,1))
    GL.glColor3f(*color)
    GL.glBegin(GL.GL_LINES)
    GL.glVertex2f(startpos[0], startpos[1])
    GL.glVertex2f(endpos[0], endpos[1])
    GL.glEnd()

def lines(surface, color, closed, points, width=1):
    for p1, p2 in zip(points, points[1:]):
        line(surface, color, p1, p2, width)
    if closed:
        line(surface, color, points[-1], points[0], width)
    
from math import pi, sin, cos
def arc(surface, color, rect, angle_start, angle_stop, width=0):
    # TODO implement
    x,y = rect.center
    rx = rect.width/2.0
    ry = rect.height/2.0
    
    t0 = angle_start
    sweep = angle_stop
    t = t0
    r = rect.width/2.0
    n = int(3*r) #/* # of segments */
    dt = (sweep - t0)/ n
    GL.glColor3f(*color)
    GL.glLineWidth(max(width,1))
    GL.glBegin(GL.GL_LINE_STRIP)
    for i in xrange(n+1):
        GL.glVertex2f(x + rx*cos(t), y - ry*sin(t))
        t += dt
    GL.glEnd()


def ellipse(surface, color, rect, width=0):
    # todo implement filling the eliipse if width=0
    arc(surface, color, rect, 0, 2*pi, width)

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

def draw_font(surface, rendered_surface, pos):
    pass

def blit(surface, blit_surface, pos):
    pass

def lock(surface):
    pass

def unlock(surface):
    pass


def save(surface, filename):
    pass
