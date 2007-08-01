## /* Copyright 2007, Noam Lewis, enoughmail@googlegroups.com */
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

from Lib.Point import Point
import math

def get_default(val, default):
    if val is None:
        return default
    return val


class MovingValue(object):
    def __init__(self, current, final, step=0.3, delta=0.1):
        self._current = current
        self._final = final
        self.step = step
        self.done = False
        self.delta = delta

    def get_final(self):
        return self._final
    def set_final(self, value):
        self._final = value
        self.done = False
    final = property(get_final, set_final)
    def get_current(self):
        return self._current
    def set_current(self, value):
        self._current = value
        self.done = False
    current = property(get_current, set_current)

    def reset(self):
        self.done = False
        
    def update(self):
        if self.done:
            return
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

    def verify_exists(self, name):
        if name not in self.__dict__['_allowed_names']:
            raise AttributeError("%s can not hold attribute %s" % (self.__dict__['_name'], name))
        
    def __getattr__(self, name):
        self.verify_exists(name)
        return self.__dict__['_params'][name]

    def __setattr__(self, name, value):
        self.verify_exists(name)
        self.__dict__['_params'][name] = value

class MovingLine(MovingValue):
    # like MovingValue but for a list of points the represent a line
    def update(self):
        if not self.current:
            self.current = [Point(0,0) for p in self.final]
        else:
            len_diff = len(self.final) - len(self.current)
            if len_diff < 0:
                # delete intermediate points until they are the same length
                for i in xrange(-len_diff):
                    self.current.pop(len(self.current)/2)
            elif len_diff > 0:
                for i in xrange(len_diff):
                    self.current.insert(1, self.current[0].copy())
                    
        for current_p, final_p in zip (self.current, self.final):
            current_p += (final_p - current_p) * self.step

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
    pygame.draw.polygon(surface, color, [p.as_tuple() for p in triangle], width)

def n_point_regular_polygon(n, radius, center, phase=0):
    twopi = 2*math.pi
    for i in xrange(n):
        angle = twopi/n*i + phase
        yield Point.from_polar(angle, radius) + center

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

    coors = [Point(0, 0),
             Point(surface.get_width(), 0),
             Point(0, surface.get_height()),
             Point(surface.get_width(), surface.get_height())]
    coors = [p.rotate(angle) for p in coors]

    leftmost = min(p.x for p in coors)
    topmost = min(p.y for p in coors)

    # pygame.transform.rotate makes a larger adjusted surface where
    # leftmost/topmost are 0,0:
    adjust = Point(-leftmost, -topmost)
    coors = [p + adjust for p in coors]
    return rt, coors

def point_in_box(point, box_origin, box_size):
    p = box_origin
    s = box_size
    if ((point.x > p.x)
        and (point.y > p.y)
        and (point.x < p.x + s.x)
        and (point.y < p.y + s.y)):
        return True
    
def point_near_polyline(point, line_points, delta=3):
    if len(line_points) < 2:
        return False
    i = 0
    p = Point(0,0)
    s = Point(0,0)
    while i < len(line_points) - 1:
        p1 = line_points[i]
        p2 = line_points[i+1]
        i += 1

        s.x = abs(p1.x - p2.x) + 8*delta
        s.y = abs(p1.y - p2.y) + 8*delta
        p.x = min(p1.x, p2.x) - 4*delta
        p.y = min(p1.y, p2.y) - 4*delta

        if point_in_box(point, p, s):
            d = dist_from_line(point, p1, p2)
            if d < delta:
                return True
        
    return False

def dist_from_line(p0, p1, p2, delta=0.0000001):
    # from http://mathworld.wolfram.com/Point-LineDistance3-Dimensional.html
    p1_0 = p1-p0
    p2_1 = p2-p1
    p1_0_n = (p1_0).norm()
    p2_1_n = (p2_1).norm()

    d_sqrd = ((p1_0_n**2 * p2_1_n**2 - (p1_0*p2_1).norm()**2)
              / (p2_1_n**2))
    if d_sqrd < delta:
        # silly heuristic 
        return d_sqrd
    
    d = math.sqrt(d_sqrd)
    return d
                
