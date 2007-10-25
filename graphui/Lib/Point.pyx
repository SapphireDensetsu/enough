# Copyright (c) 2007 Enough Project.
# See LICENSE for details.

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

from __future__ import division
import pygame


from math import atan2, sin, cos, pi

class VectorsNotColinear(Exception): pass

cdef extern from "math.h":
    double fabs(double x)
cdef extern from "math.h":
    double fmin(double x, double y)
cdef extern from "math.h":
    double sqrt(double x)

cdef class Point:
    cdef public double x, y
    def __init__(self, t):
        self.x, self.y = t
    def __getinitargs__(self):
        return (tuple(self),)
    def __repr__(self):
        return '%s(x=%r, y=%r)' % (self.__class__.__name__, self.x, self.y)
    
    def __add__(self, Point other):
        return Point((self.x+other.x, self.y+other.y))
    def __iadd__(self, Point other):
        self.x = self.x + other.x
        self.y = self.y + other.y
        return self
    def __neg__(self):
        return Point((-self.x, -self.y))
    def __sub__(self, Point other):
        return Point((self.x-other.x, self.y-other.y))
    def __isub__(self, Point other):
        self.x = self.x - other.x
        self.y = self.y - other.y
        return self
    def __mul__(self, value):
        if isinstance(value, self.__class__):
            other = value
            return Point((self.x*other.x, self.y*other.y))
        else:
            num = value
            return Point((self.x*num, self.y*num))
        
    def __div__(self, value):
        cdef Point other
        if isinstance(value, self.__class__):
            other = value
            return Point((self.x/other.x, self.y/other.y))
        else:
            return Point((self.x/value, self.y/value))

    def __cmp__(self, other):
        if not isinstance(other, Point):
            return -1
        return cmp(tuple(self), tuple(other))

    def __abs__(self):
        return sqrt(self.x*self.x + self.y*self.y)
    def norm(self):
        return abs(self)

    def __hash__(self):
        raise TypeError, "%s objects are unhashable" % (self.__class__.__name__,)

    def __getitem__(self, int index):
        if index == 0:
            return self.x
        elif index == 1:
            return self.y
        else:
            raise IndexError, index
    
    def dot_product(self, Point other):
        return self.x*other.x + self.y*other.y
    
    def angle(self):
        return atan2(self.y, self.x)

    def rotate(self, double angle):
        return from_polar(self.angle()+angle, abs(self))

    def copy(self):
        return Point((self.x, self.y))
    
    def find_linear_coefficient(self, other, delta=0.1**10):
        # Finds scalar t such that self = other*t
        # returns None if ANY number is good (could happen if both points = 0,0,0)
        # If one coordinate is off by delta, ignore and find near coefficient
        res = []
        for my_coord, other_coord in zip(self.as_tuple(dimensions=3),
                                         other.as_tuple(dimensions=3)):
            if abs(other_coord) < delta:
                if abs(my_coord) < delta:
                    continue
                raise VectorsNotColinear
                    
            res.append(my_coord / other_coord)

        if not res:
            # All zeros
            return None

        for p in res[1:]:
            if abs(p - res[0]) > delta:
                raise VectorsNotColinear
        return res[0]
        
def from_polar(angle, radius):
    return Point((cos(angle), sin(angle)))*radius

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
        raise ValueError, "Line can't be defined by a single point"
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
    cdef double x1, x2, y1, y2, cdelta
    cdef int i

    cdelta = delta
    
    if len(line_points) < 2:
        return False
    
    i = 0
    p = Point((0,0))
    s = Point((0,0))
    while i < len(line_points) - 1:
        p1 = line_points[i]
        p2 = line_points[i+1]
        i = i + 1

        x1 = p1.x
        y1 = p1.y
        x2 = p2.x
        y2 = p2.y
        
        s.x = fabs(x1 - x2) + 8*cdelta
        s.y = fabs(y1 - y2) + 8*cdelta
        p.x = fmin(x1, x2) - 4*cdelta
        p.y = fmin(y1, y2) - 4*cdelta

        if point_in_box(point, p, s):
            d = dist_from_line(point, p1, p2)
            if d < cdelta:
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
                
