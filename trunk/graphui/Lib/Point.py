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

from __future__ import division
import pygame


from math import atan2, sqrt, sin, cos, pi

class VectorsNotColinear(Exception): pass

class Point(object):
    def __init__(self, (x, y)=(0,0)):
        self.x = x
        self.y = y

    def __getinitargs__(self):
        return (tuple(self),)
    
    def __repr__(self):
        return '%s(%r, %r)' % (self.__class__.__name__, self.x, self.y)
    
    def __add__(self, other):
        return self.__class__((self.x+other.x, self.y+other.y))
    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        return self
    def __neg__(self):
        return self.__class__((-self.x, -self.y))
    def __sub__(self, other):
        return self.__class__((self.x-other.x, self.y-other.y))
    def __isub__(self, other):
        self.x-=other.x
        self.y-=other.y
        return self
    def __mul__(self, value):
        if isinstance(value, self.__class__):
            other = value
            return self.__class__((self.x*other.x, self.y*other.y))
        else:
            num = value
            return self.__class__((self.x*num, self.y*num))
        
    def __div__(self, value):
        if isinstance(value, self.__class__):
            other = value
            return self.__class__((self.x/other.x, self.y/other.y))
        else:
            return self.__class__((self.x/value, self.y/value))

    def __cmp__(self, other):
        # This used to unallowed, but since we are using Pyrex also which doesn't support ne/eq, we allow this
        if not isinstance(other, Point):
            return -1
        return cmp(tuple(self), tuple(other))

    def __abs__(self):
        return sqrt(self.x*self.x + self.y*self.y)
    norm = __abs__
    
    def dot_product(self, other):
        return self.x*other.x + self.y*other.y
    
    def __getitem__(self, index):
        if index == 0:
            return self.x
        elif index == 1:
            return self.y
        else:
            raise IndexError(index)
        
    def angle(self):
        return atan2(self.y, self.x)

    def rotate(self, angle):
        return self.__class__.from_polar(self.angle()+angle, self.norm())

    @classmethod
    def from_polar(cls, angle, radius):
        return cls((cos(angle), sin(angle)))*radius

    def copy(self):
        return self.__class__((self.x, self.y))
    
    def find_linear_coefficient(self, other, delta=0.1**10):
        # Finds scalar t such that self = other*t
        # returns None if ANY number is good (could happen if both points = 0,0,0)
        # If one coordinate is off by delta, ignore and find near coefficient
        res = []
        for my_coord, other_coord in zip(tuple(self),
                                         tuple(other)):
            if abs(other_coord) < delta:
                if abs(my_coord) < delta:
                    continue
                raise VectorsNotColinear()
                    
            res.append(my_coord / other_coord)

        if not res:
            # All zeros
            return None

        for p in res[1:]:
            if abs(p - res[0]) > delta:
                raise VectorsNotColinear()
        return res[0]
        

# compatibility with Pyrex limitations
from_polar = Point.from_polar


def find_vect_from_point_to_line(point, src, dest):
    # src and dest are two points on the line
    # Finds the vector pointing from point to the nearest point on the line
    u = src
    v = dest - src
    w = point
    t = (((u-w).dot_product(v))/(v.dot_product(v)))
    e = u - w - v * t
    return e

    
def point_in_line_segment(point, src, dest, delta=0.1**15):
    if src == dest:
        raise ValueError("Line can't be defined by a single point")
    v = dest - src
    u = point - src
    try:
        t = u.find_linear_coefficient(v)
    except VectorsNotColinear:
        return False
    if t is None or (t >= 0 and t <= 1):
        return True
    return False


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
    p = Point((0,0))
    s = Point((0,0))
    while i < len(line_points) - 1:
        p1 = line_points[i]
        p2 = line_points[i+1]
        i = i + 1

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

    d = sqrt(d_sqrd)
    return d
                
