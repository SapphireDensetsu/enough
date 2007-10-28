# Copyright (c) 2007 Enough Project.
# See LICENSE for details.

import pygame
from OpenGL import GL


def make_chars(pfont):
    chars = {}
    for i in xrange(256):
        s = chr(i)
        try:
            letter_render = pfont.render(s, 1, (255,255,255), (0,0,0))
        except:
            letter = None
            letter_w = letter_h = 0
        else:
            letter = pygame.image.tostring(letter_render, 'RGBA', 1)
            letter_w, letter_h = letter_render.get_size()
            
        chars[s] = letter, letter_w, letter_h
    return chars

def calc_size(line, chars):
    pos = [0,0]
    for c in line:
        data, w, h = chars[c]
        pos[0] += w
        pos[1] = max(pos[1], h)
    return pos
    
def draw_chars(line, chars, color, pos):
    r,g,b = [x/255.0 for x in color]
    GL.glPushMatrix()
    GL.glPixelTransferf(GL.GL_RED_SCALE, r)
    GL.glPixelTransferf(GL.GL_GREEN_SCALE, g)
    GL.glPixelTransferf(GL.GL_BLUE_SCALE, b)
    GL.glAlphaFunc(GL.GL_GREATER, 0)
    pos = list(map(int, pos))
    for c in line:
        data, w, h = chars[c]
        if data is None:
            continue # ignore unprintable chars
        GL.glRasterPos2i(pos[0], pos[1]+h)
        GL.glDrawPixels(w, h, GL.GL_RGBA, GL.GL_UNSIGNED_BYTE, data)
        pos[0] += w 
    GL.glPopMatrix()
        



