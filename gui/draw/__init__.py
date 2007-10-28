# Copyright (c) 2007 Enough Project.
# See LICENSE for details.

import backend

from backend import get_font, set_mode, fill

import rounded
import offset

def rect(surface, color, rect, width=0):
    rect = offset.rect_offset(rect)
    return backend.rect(surface, color, rect, width)

def line(surface, color, startpos, endpos, width=1):
    startpos = offset.pos_offset(startpos)
    endpos = offset.pos_offset(endpos)
    return backend.line(surface, color, startpos, endpos, width)

def arc(surface, color, rect, angle_start, angle_stop, width=0):
    rect = offset.rect_offset(rect)
    return backend.arc(surface, color, rect, angle_start, angle_stop, width)


def draw_font(surface, fakefont_surface, pos):
    pos = offset.pos_offset(pos)
    return backend.draw_font(surface, fakefont_surface, pos)

