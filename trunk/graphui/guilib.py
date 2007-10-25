# Copyright (c) 2007 Enough Project.
# See LICENSE for details.

## /* Copyright 2007, Eyal Lotem, Noam Lewis, enoughmail@googlegroups.com */
## /*
##     This file is part of Enough.

##     Enough is free software; you can redistribute it and/or modify
##     it under the terms of the GNU General Public License as published by
##     the Free Software Foundation; either version 3 of the License, or
##     (at your option) any later version.

##     Enough is distributed in the hope that it will be useful,
##     but WITHOUT ANY WARRANTY; without even the implied warranty of
##     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##     GNU General Public License for more details.

##     You should have received a copy of the GNU General Public License
##     along with this program.  If not, see <http://www.gnu.org/licenses/>.
## */

from Lib.Point import Point, from_polar
import math

def get_default(val, default):
    if val is None:
        return default
    return val


class MovingValue(object):
    def __init__(self, factory, final=None, step=0.3, delta=0.1):
        self.factory = factory
        self._current = None
        self._final = final
        if self._final is None:
            self._final = factory()
        self.step = step
        self.done = False
        self.delta = delta

    def get_final(self):
        if self._current is None:
            self._current = self.factory(self._final)
        return self._final
    def set_final(self, value):
        self._final = value
        self.reset()
    final = property(get_final, set_final)
    def get_current(self):
        return self._current
    def set_current(self, value):
        self._current = value
        self.done = False
    current = property(get_current, set_current)

    def reset(self):
        self.done = False
        if self._current is None:
            self._current = self.factory(self._final)
        
    def update(self):
        if self.done:
            return
        if self._current is None:
            self._current = self.factory(self._final)
        diff = (self._final - self._current)
        if abs(diff) < self.delta:
            self.done = True
            return
        self.current += diff * self.step
        
        
class ParamHolder(object):
    def __init__(self, allowed_names, name=None):
        self.__dict__['_allowed_names'] = allowed_names
        self.__dict__['_name'] = get_default(name, self.__class__.__name__)
        self.__dict__['_params'] = {}

    def __getinitargs__(self):
        return (self.__dict__['_allowed_names'], self.__dict__['_name'])
    def __getstate__(self):
        return self.__dict__
    def __setstate__(self, dict):
        self.__dict__.update(dict)
        
    def verify_exists(self, name):
        if name not in self.__dict__['_allowed_names']:
            raise AttributeError("%s can not hold attribute %s" % (self.__dict__['_name'], name))
        
    def __getattr__(self, name):
        self.verify_exists(name)
        return self.__dict__['_params'][name]

    def __setattr__(self, name, value):
        self.verify_exists(name)
        self.__dict__['_params'][name] = value

    def add_allowed_name(self, name):
        self.__dict__['_allowed_names'].append(name)
        
class MovingLine(MovingValue):
    # like MovingValue but for a list of points the represent a line
    def update(self):
        if self.done:
            return True
        if not self.current:
            self.current = [Point((0,0)) for p in self.final]
        else:
            len_diff = len(self.final) - len(self.current)
            if len_diff < 0:
                # delete intermediate points until they are the same length
                for i in xrange(-len_diff):
                    self.current.pop(len(self.current)/2)
            elif len_diff > 0:
                for i in xrange(len_diff):
                    self.current.insert(1, self.current[0].copy())

        num_done = 0
        for current_p, final_p in zip(self.current, self.final):
            diff = (final_p - current_p)
            if abs(diff) < self.delta:
                num_done += 1
                continue
            current_p += diff * self.step
        if num_done == len(self.final):
            self.done = True

import pygame

def paint_arrowhead_by_direction(surface, color, src, target_pos, size=7, width=0):
    """src is only used for angle calculation purposes.
    target_pos is the destination triangle's tip's position"""
    direction = target_pos - src
    normalized = direction * (1/direction.norm())
    angle = direction.angle()
    center = target_pos - (normalized * size)
    return paint_arrowhead(surface, color, center, angle, size=size, width=width)
    
def paint_arrowhead(surface, color, center, angle, size=7, width=0):
    triangle = n_point_regular_polygon(3, size, center, angle)
    points = [tuple(p) for p in triangle]
    pygame.draw.polygon(surface, color, points, width)
    return color, points, width # For re-use without calculation

def repaint_arrowhead(surface, color, points, width):
    pygame.draw.polygon(surface, color, points, width)
    
def n_point_regular_polygon(n, radius, center, phase=0):
    twopi = 2*math.pi
    for i in xrange(n):
        angle = twopi/n*i + phase
        yield from_polar(angle, radius) + center

pygame_reverse_key_map = {}
def build_reverse_pygame_key_map():
    import pygame
    global pygame_reverse_key_map
    for name in pygame.__dict__:
        if name.startswith("K_"):
            pygame_reverse_key_map[pygame.__dict__[name]] = name
build_reverse_pygame_key_map()

def rotate_surface(surface, angle):
    rt = pygame.transform.rotate(surface, -math.degrees(angle))

    coors = [Point((0, 0)),
             Point((surface.get_width(), 0)),
             Point((0, surface.get_height())),
             Point((surface.get_width(), surface.get_height()))]
    coors = [p.rotate(angle) for p in coors]

    leftmost = min(p.x for p in coors)
    topmost = min(p.y for p in coors)

    # pygame.transform.rotate makes a larger adjusted surface where
    # leftmost/topmost are 0,0:
    adjust = Point((-leftmost, -topmost))
    coors = [p + adjust for p in coors]
    return rt, coors
