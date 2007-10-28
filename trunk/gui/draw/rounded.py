# Copyright (c) 2007 Enough Project.
# See LICENSE for details.

import pygame
import backend
from math import pi

def _rounded_rect(surface, color, rect, width, corner_radius):
    backend.lock(surface)
    rect.height -= width//2
    rect.width -= width//2
    diameter = corner_radius * 2
    for offset, angles, corner in (((0,         0),        (pi/2, pi), rect.topleft,),
                                   ((-diameter, 0),        (0,  pi/2), rect.topright),
                                   ((-diameter,-diameter), (3./2*pi, 2*pi), rect.bottomright),
                                   ((0,        -diameter), (pi, 3./2*pi), rect.bottomleft),
                                   ):
        corner = map(lambda a,b:a+b, offset, corner)
        corner_rect = pygame.Rect(corner[0], corner[1], diameter, diameter)
        backend.arc(surface, color, corner_rect, angles[0], angles[1], width)
        

    line_dist = corner_radius
    for p1, p2 in (((rect.topleft[0] + line_dist, rect.topleft[1]),
                    (rect.topright[0] - line_dist, rect.topright[1])),
                   ((rect.topright[0], rect.topright[1] + line_dist),
                    (rect.bottomright[0], rect.bottomright[1] - line_dist)),
                   ((rect.bottomright[0] - line_dist, rect.bottomright[1]),
                    (rect.bottomleft[0] + line_dist, rect.bottomleft[1])),
                   ((rect.bottomleft[0], rect.bottomleft[1] - line_dist),
                    (rect.topleft[0], rect.topleft[1] + line_dist)),
                   ):
        backend.line(surface, color, p1, p2, width)
    backend.unlock(surface)

import offset

def rounded_rect(surface, color, rect, width, corner_radius):
    rect = offset.rect_offset(rect)
    _rounded_rect(surface, color, rect, width, corner_radius)
