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
        return sqrt(self.x*self.x + self.y*self.y)

    def update_from_tuple(self, (x,y)):
        self.x = x
        self.y = y
        
    @classmethod
    def from_polar(cls, angle, radius):
        return cls(cos(angle), sin(angle))*radius

    @classmethod
    def from_tuple(cls, (x, y)):
        return cls(x, y)

    def copy(self):
        return Point(self.x, self.y, self.z)
