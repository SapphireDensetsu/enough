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


from math import atan2, sqrt, sin, cos, pi

class VectorsNotColinear(Exception): pass

class Point(object):
    def __init__(self, x,y,z=0):
        self.x = x
        self.y = y
        self.z = z
    def __repr__(self):
        return '<%s, x=%r, y=%r, z=%r>' % (self.__class__.__name__, self.x, self.y, self.z)
    
    def __add__(self, other):
        return Point(self.x+other.x, self.y+other.y, self.z+other.z)
    def __iadd__(self, other):
        self.x+=other.x
        self.y+=other.y
        self.z+=other.z
        return self
    def __neg__(self):
        return Point(-self.x, -self.y, -self.z)
    def __sub__(self, other):
        return Point(self.x-other.x, self.y-other.y, self.z-other.z)
    def __isub__(self, other):
        self.x-=other.x
        self.y-=other.y
        self.z-=other.z
        return self
    def __mul__(self, value):
        if isinstance(value, self.__class__):
            other = value
            return Point(self.x*other.x, self.y*other.y, self.z*other.z)
        else:
            num = value
            return Point(self.x*num, self.y*num, self.z*num)
        
    def __div__(self, value):
        if isinstance(value, self.__class__):
            other = value
            return Point(self.x/other.x, self.y/other.y, self.z/other.z)
        else:
            return Point(self.x/value, self.y/value, self.z/value)

    def __eq__(self, other):
        return other.x == self.x and other.y == self.y and other.z == self.z

    def __cmp__(self, other):
        raise ValueError("Can't compare vectors")

    def __abs__(self):
        return abs(self.as_complex()) #sqrt(self.x*self.x + self.y*self.y)
    
    def dot_product(self, other):
        return self.x*other.x + self.y*other.y + self.z*other.z
    
    def as_tuple(self, dimensions=2):
        return (self.x,self.y,self.z)[:dimensions]
        
    def angle(self):
        return atan2(self.y,self.x)
    def norm(self):
        return abs(self)

    def as_complex(self):
        return self.x + self.y * 1j
    
    def update_from_tuple(self, (x,y)):
        self.x = x
        self.y = y

    def rotate(self, angle):
        return self.__class__.from_polar(self.angle()+angle, self.norm())

    @classmethod
    def from_polar(cls, angle, radius):
        return cls(cos(angle), sin(angle))*radius

    @classmethod
    def from_tuple(cls, (x, y)):
        return cls(x, y)

    def copy(self):
        return Point(self.x, self.y, self.z)
    
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
                raise VectorsNotColinear()
                    
            res.append(my_coord / other_coord)

        if not res:
            # All zeros
            return None

        for p in res[1:]:
            if abs(p - res[0]) > delta:
                raise VectorsNotColinear()
        return res[0]
        



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

