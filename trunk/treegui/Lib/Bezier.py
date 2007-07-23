# Hitched from WikiPedia
## /*
## cp is a 4 element array where:
## cp[0] is the starting point, or P0 in the above diagram
## cp[1] is the first control point, or P1 in the above diagram
## cp[2] is the second control point, or P2 in the above diagram
## cp[3] is the end point, or P3 in the above diagram
## t is the parameter value, 0 <= t <= 1
## */
from Point import Point

def PointOnCubicBezier(cp, t):
    #/* calculate the polynomial coefficients */
    cx = 3.0 * (cp[1].x - cp[0].x)
    bx = 3.0 * (cp[2].x - cp[1].x) - cx
    ax = cp[3].x - cp[0].x - cx - bx

    cy = 3.0 * (cp[1].y - cp[0].y)
    by = 3.0 * (cp[2].y - cp[1].y) - cy
    ay = cp[3].y - cp[0].y - cy - by

    #/* calculate the curve point at parameter value t */

    tSquared = t * t
    tCubed = tSquared * t

    x= (ax * tCubed) + (bx * tSquared) + (cx * t) + cp[0].x
    y= (ay * tCubed) + (by * tSquared) + (cy * t) + cp[0].y

    return Point(x,y)

def rec_point_on_curve(cp, t):
    # From wikipedia - recursive definition for n-degree bezier curve
    # B(t) = Bp0..pn(t) = (1-t)Bp0..pn-1(t) + t*Bp1..pn(t)
    assert len(cp) >= 4, "I implemented only 4-degree or higher...you can do the rest."
    if len(cp) == 4:
        return PointOnCubicBezier(cp, t)
    return point_on_curve(cp[:-1], t)*(1-t) + point_on_curve(cp[1:], t)*t

from Func import cached

@cached
def factorial(n):
    r = 1
    for i in xrange(2,n+1):
        r *= i
    return r

@cached
def choose(k, n):
    assert k <= n, "K must be < N"
    return factorial(n)/(factorial(k)*factorial(n-k))
    
def nonrec_point_on_curve(cp, t):
    # Non-recursive implementation, also according to formula from wikipedia
    n = len(cp) - 1
    p = Point(0,0)
    for i in xrange(n+1):
        p += cp[i]*float(choose(i, n)) * ((1-t)**(n-i)) * (t**i)
    return p

# It is not clear which is faster. I didn't check.
point_on_curve = nonrec_point_on_curve
    
def Bezier(cp, numberOfPoints):
    dt = 1.0 / ( numberOfPoints - 1 )
    curve = []
    for i in xrange(numberOfPoints):
        curve.append(point_on_curve( cp, i*dt ))
    return curve

