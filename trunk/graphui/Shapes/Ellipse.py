from __future__ import division

import math
from Lib.Point import Point


class Ellipse(object):
    def __init__(self, rect):
        self.rect = rect
    def __getinitargs__(self):
        return (self.rect,)

    def paint(self, offset, surface, fore_color, back_color):
        import pygame
        rect = self.rect.x+offset.x, self.rect.y+offset.y, self.rect.w, self.rect.h
        pygame.draw.ellipse(surface, back_color, rect, 0)
        if rect[2] > 5 and rect[3] > 5:
            # otherwise we get a pygame error for using a width that's larger than the elipse radius
            pygame.draw.ellipse(surface, fore_color, rect, 2)
        
    def intersections(self, src, dest):
        """Returns the point of the intersection between the infinite
        line defined by (src, dest) and this shape, or None if there
        is no such intersection"""
        if src == dest:
            raise ValueError("Line is not defined by a single point")
        cx, cy = self.rect.center
        w, h = self.rect.size
        x1, y1 = src.x, src.y
        x2, y2 = dest.x, dest.y
        if x1==x2:
            # x = my + n
            m = 1. * (x2-x1)/(y2-y1)
            n = 1. * (x1*y2-x2*y1)/(y2-y1)

            s = (-4.*(n**2)-8*cy*m*n+8*cx*n + (h**2-4*(cy**2))*(m**2) + 8*cx*cy*m + (w**2)-4*(cx**2))
            if s < 0:
                return
            sq = math.sqrt(s)*h*w
            div = (2.*(h**2)*(m**2)+2*(w**2))

            xexpr = 2.*(w**2)*n+2*cx*(h**2)*(m**2)+2*cy*(w**2)*m
            yexpr = 2.*(h**2)*m*n-2*cx*(h**2)*m-2*cy*(w**2)
            
            i1 = Point((-(m*sq-xexpr)/div, -(sq+yexpr)/div))
            i2 = Point((-(-m*sq-xexpr)/div, -(-sq+yexpr)/div))
        else:
            # y = mx + n
            m = (y2-y1)/(x2-x1)
            n = (x2*y1-x1*y2)/(x2-x1)

            s = (-4*(n**2)-8*cx*m*n+8*cy*n+(w**2)*(m**2)-4*(cx**2)*(m**2)+8*cx*cy*m+(h**2)-4*(cy**2))
            if s < 0:
                return
            sq = math.sqrt(s)*h*w
            div = (2.*(w**2)*(m**2)+2*(h**2))
            xexpr = 2.*(w**2)*m*n-2*cy*(w**2)*m-2*cx*(h**2)
            yexpr1 = 2.*cx*(h**2)
            yexpr2 = 2.*(h**2)*n+2*cy*(w**2)*(m**2)
            i1 = Point((-(sq+xexpr)/div, (m*(yexpr1-sq)+yexpr2)/div))
            i2 = Point((-(-sq+xexpr)/div,(m*(yexpr1+sq)+yexpr2)/div))

        margin_error = 0.0001
        for i in [i1, i2]:
            if (((x1-margin_error <= i.x <= x2+margin_error) or
                 (x2-margin_error <= i.x <= x1+margin_error)) and
                ((y1-margin_error <= i.y <= y2+margin_error)) or
                (y2-margin_error <= i.y <= y1+margin_error)):
                yield i

    # Dead code, delete:?
    def inside(self, p):
        cx, cy = self.rect.center
        return ((2.*(p.x-cx)/self.rect.width)**2 + (2.*(p.y-cy)/self.rect.height)**2 <= 1)



def _test_speed(num=10):
    import pygame
    import random
    def rand_point(n=5):
        return Point((random.random()*n*2-n,
                      random.random()*n*2-n))
    es = []
    for i in xrange(200):
        es.append(Ellipse(pygame.Rect(tuple(rand_point()), tuple(rand_point()))))

    import time
    t = time.time()
    for i in xrange(num):
        for e in es:
            e.intersections(rand_point(10), rand_point(10))
    print 'Time:', time.time() - t, ',', num*i, 'intersections'
        