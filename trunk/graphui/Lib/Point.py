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

import pygame

from AttrDict import AttrDict

from math import atan2, sqrt, sin, cos, pi

class Point(AttrDict):
    allowed_fields = [('x',),
                      ('y',),
                      ('z',0),
                      ]
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
    def as_tuple(self, with_z=False):
        return (self.x,self.y)
    def angle(self):
        return atan2(self.y,self.x)
    def norm(self):
        return abs(self.as_complex()) #sqrt(self.x*self.x + self.y*self.y)

    def as_complex(self):
        return self.x + 1j * self.y
    
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
