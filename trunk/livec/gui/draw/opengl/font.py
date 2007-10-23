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

def draw_chars(line, chars, color, pos):
    GL.glPushMatrix()
    pos = list(pos)
    for c in line:
        data, w, h = chars[c]
        GL.glRasterPos2i(pos[0], pos[1])
        GL.glDrawPixels(w, h, GL.GL_RGBA, GL.GL_UNSIGNED_BYTE, data)
        pos[0] += w
    GL.glPopMatrix()
        



