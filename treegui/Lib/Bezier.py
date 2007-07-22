# Hitched from WikiPedia
## /*
## cp is a 4 element array where:
## cp[0] is the starting point, or P0 in the above diagram
## cp[1] is the first control point, or P1 in the above diagram
## cp[2] is the second control point, or P2 in the above diagram
## cp[3] is the end point, or P3 in the above diagram
## t is the parameter value, 0 <= t <= 1
## */

def PointOnCubicBezier(cp, t):
    #/* calculate the polynomial coefficients */
    cx = 3.0 * (cp[1][0] - cp[0][0])
    bx = 3.0 * (cp[2][0] - cp[1][0]) - cx
    ax = cp[3][0] - cp[0][0] - cx - bx

    cy = 3.0 * (cp[1][1] - cp[0][1])
    by = 3.0 * (cp[2][1] - cp[1][1]) - cy
    ay = cp[3][1] - cp[0][1] - cy - by

    #/* calculate the curve point at parameter value t */

    tSquared = t * t
    tCubed = tSquared * t

    x= (ax * tCubed) + (bx * tSquared) + (cx * t) + cp[0][0]
    y= (ay * tCubed) + (by * tSquared) + (cy * t) + cp[0][1]

    return x,y

## /*
##  ComputeBezier fills an array of Point2D structs with the curve   
##  points generated from the control points cp. Caller must 
##  allocate sufficient memory for the result, which is 
##  <sizeof(Point2D) numberOfPoints>

def Bezier(cp, numberOfPoints):
    dt = 1.0 / ( numberOfPoints - 1 )
    curve = []
    for i in xrange(numberOfPoints):
        curve.append(PointOnCubicBezier( cp, i*dt ))
    return curve
