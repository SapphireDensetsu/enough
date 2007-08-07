from Lib.Point import Point


cdef extern from "math.h":
    double sqrt(double x)
    
class Ellipse(object):
    def __init__(self, rect):
        self.rect = rect
    def __getinitargs__(self):
        return (self.rect,)

    def paint(self, offset, surface):
        rect = self.rect.x+offset.x, self.rect.y+offset.y, self.rect.w, self.rect.h
        pygame.draw.ellipse(surface, back_color, rect, 0)
        if rect.size[0] > 5 and rect.size.y > 5:
            # otherwise we get a pygame error for using a width that's larger than the elipse radius
            pygame.draw.ellipse(surface, self.params.fore_color, rect, 2)
        
    
    def intersections(self, src, dest, margin_error = 0.0001):
        cdef double cx, cy, w, h, x1, y1, x2, y2, m, n, s, sq, div, xexpr, yexpr, yexpr1, yexpr2, cmargin_error

        # powers
        cdef double n_2, m_2, h_2, w_2, cx_2, cy_2

        cdef double tempx, tempy
        
        cmargin_error = margin_error
        
        """Returns the point of the intersection between the infinite
        line defined by (src, dest) and this shape, or None if there
        is no such intersection"""
        if src == dest:
            raise ValueError, "Line is not defined by a single point"
        cx, cy = self.rect.center
        w, h = self.rect.size
        x1, y1 = src.x, src.y
        x2, y2 = dest.x, dest.y
        if x1==x2:
            # x = my + n
            m = 1. * (x2-x1)/(y2-y1)
            n = 1. * (x1*y2-x2*y1)/(y2-y1)

            n_2 = n*n
            m_2 = m*m
            h_2 = h*h
            w_2 = w*w
            cx_2 = cx*cx
            cy_2 = cy*cy
            
            s = (-4.*(n_2)-8*cy*m*n+8*cx*n + (h_2-4*(cy_2))*(m_2) + 8*cx*cy*m + (w_2)-4*(cx_2))
            if s < 0:
                return tuple()
            sq = sqrt(s)*h*w
            div = (2.*(h_2)*(m_2)+2*(w_2))

            xexpr = 2.*(w_2)*n+2*cx*(h_2)*(m_2)+2*cy*(w_2)*m
            yexpr = 2.*(h_2)*m*n-2*cx*(h_2)*m-2*cy*(w_2)
            
            i1 = Point((-(m*sq-xexpr)/div, -(sq+yexpr)/div))
            i2 = Point((-(-m*sq-xexpr)/div, -(-sq+yexpr)/div))
        else:
            # y = mx + n
            m = (y2-y1)/(x2-x1)
            n = (x2*y1-x1*y2)/(x2-x1)

            n_2 = n*n
            m_2 = m*m
            h_2 = h*h
            w_2 = w*w
            cx_2 = cx*cx
            cy_2 = cy*cy

            s = (-4*(n_2)-8*cx*m*n+8*cy*n+((w_2))*((m_2))-4*((cx_2))*((m_2))+8*cx*cy*m+((h_2))-4*((cy_2)))
            if s < 0:
                return tuple()
            sq = sqrt(s)*h*w
            div = (2.*((w_2))*((m_2))+2*((h_2)))
            xexpr = 2.*((w_2))*m*n-2*cy*((w_2))*m-2*cx*((h_2))
            yexpr1 = 2.*cx*((h_2))
            yexpr2 = 2.*((h_2))*n+2*cy*((w_2))*((m_2))
            i1 = Point((-(sq+xexpr)/div, (m*(yexpr1-sq)+yexpr2)/div))
            i2 = Point((-(-sq+xexpr)/div,(m*(yexpr1+sq)+yexpr2)/div))

        res = []
        for i in [i1, i2]:
            tempx = i.x
            tempy = i.y
            if (((x1-cmargin_error <= tempx <= x2+cmargin_error) or
                 (x2-cmargin_error <= tempx <= x1+cmargin_error)) and
                ((y1-cmargin_error <= tempy <= y2+cmargin_error)) or
                (y2-cmargin_error <= tempy <= y1+cmargin_error)):
                res.append(i)
        return tuple(res)

    # Dead code, delete:?
    def inside(self, p):
        cx, cy = self.rect.center
        return ((2.*(p.x-cx)/self.rect.width)**2 + (2.*(p.y-cy)/self.rect.height)**2 <= 1)

