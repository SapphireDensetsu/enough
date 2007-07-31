from __future__ import division

import math
from Lib.Point import Point, VectorsNotColinear

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


class Circle(object):
    def __init__(self, center, radius):
        self.center = center
        self.radius = radius

    def intersections(self, src, dest, delta=0.1**15):
        if src == dest:
            raise ValueError("Line can't be defined by a single point")
        v = (dest-src)
        e = find_vect_from_point_to_line(self.center, src, dest)
        d = self.radius**2 - e.dot_product(e)
        if d < 0:
            # The distance of the line from center of circle, is
            # greater than radius.  The line does not intersect.
            return tuple()
        b1 = v * (math.sqrt(d) / v.norm())
        p1 =  b1 + self.center + e
        p2 = -b1 + self.center + e
        res = [point for point in (p1, p2)
               if point_in_line_segment(point, src,dest)]
        return tuple(res)

_unit_circle = Circle(Point(0,0), 1)

class Ellipse(object):
    def __init__(self, rect):
        self.rect = rect
        
    def intersections(self, src, dest, delta=0.1**15):
        """Returns the point of the intersection between the infinite
        line defined by (src, dest) and this shape, or None if there
        is no such intersection"""
        if src == dest:
            raise ValueError("Line can't be defined by a single point")
        if self.rect.width == 0 or self.rect.height == 0:
            return tuple()
        
        # Squish the line to reflect intersections on us if we were a unit circle.
        c = Point(*self.rect.center)
        def squish_point(p):
            tp = p - c
            return Point(tp.x/self.rect.width*2, tp.y/self.rect.height*2)
        def unsquish_point(p):
            return Point(p.x*self.rect.width/2, p.y*self.rect.height/2)  + c
            
        nsrc = squish_point(src)
        ndest = squish_point(dest)
        res = _unit_circle.intersections(nsrc, ndest, delta=delta)
        return tuple(unsquish_point(p) for p in res)



def _test_speed(num=10):
    import pygame
    def rand_point(n=5):
        return Point(random.random()*n*2-n, random.random()*n*2-n)
    es = []
    for i in xrange(200):
        es.append(Ellipse(pygame.Rect(rand_point().as_tuple(), rand_point().as_tuple())))

    import time
    t = time.time()
    for i in xrange(num):
        for e in es:
            e.intersections(rand_point(10), rand_point(10))
    print 'Time:', time.time() - t, ',', num*i, 'intersections'
        
