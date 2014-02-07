"""
Some supporting 3D geometric code

(C) James Cranch 2013-2014
"""

from math import sqrt


def bounding(x,e):
    if x>e:
        return None
    else:
        return x


def agreement(g):
    "Do all these booleans agree? If so, on what?"
    prejudice = None
    for b in g:
        if b is None:
            return None
        if prejudice is (not b):
            return None
        prejudice = b
    return prejudice


def point_in_box(p,b):
    "Is p in b?"
    (x,y,z) = p
    ((minx,maxx), (miny, maxy), (minz, maxz)) = b
    return (minx <= x < maxx) and (miny <= y < maxy) and (minz <= z < maxz)


def box_contains(b1,b2):
    "Is all of b1 in b2?"
    ((minx1,maxx1), (miny1, maxy1), (minz1, maxz1)) = b1
    ((minx2,maxx2), (miny2, maxy2), (minz2, maxz2)) = b2
    return minx2 <= minx1 and maxx1 <= maxx2 and miny2 <= miny1 and maxy1 <= maxy2 and minz2 <= minz1 and maxz1 <= maxz2


def boxes_disjoint(b1,b2):
    "Are b1 and b2 disjoint?"
    ((minx1,maxx1), (miny1, maxy1), (minz1, maxz1)) = b1
    ((minx2,maxx2), (miny2, maxy2), (minz2, maxz2)) = b2
    return maxx2 <= minx1 or maxx1 <= minx1 or maxy2 <= miny1 or maxy1 <= miny1 or maxz2 <= minz1 or maxz1 <= minz1


def union_box(b1,b2):
    "The smallest box containing b1 and b2"
    ((minx1,maxx1), (miny1, maxy1), (minz1, maxz1)) = b1
    ((minx2,maxx2), (miny2, maxy2), (minz2, maxz2)) = b2
    return ((min(minx1,minx2),max(maxx1,maxx2)),(min(miny1,miny2),max(maxy1,maxy2)),(min(minz1,minz2),max(maxz1,maxz2)))


def vertices(bounds):
    "The vertices of a box"
    (xs,ys,zs) = bounds
    for x in xs:
        for y in ys:
            for z in zs:
                yield (x,y,z)


def subboxes(bounds):
    "The eight boxes contained within a box"
    ((minx, maxx), (miny, maxy), (minz, maxz)) = bounds
    midx = (maxx+minx)/2
    midy = (maxy+miny)/2
    midz = (maxz+minz)/2
    for bx in [(minx,midx),(midx,maxx)]:
        for by in [(miny,midy),(midy,maxy)]:
            for bz in [(minz,midz),(midz,maxz)]:
                yield (bx,by,bz)


def narrow(bounds, coords):
    "Narrow down a box to an appropriate subbox"

    ((minx, maxx), (miny, maxy), (minz, maxz)) = bounds

    midx = (maxx+minx)/2
    midy = (maxy+miny)/2
    midz = (maxz+minz)/2            

    (x,y,z) = coords

    if x < midx:
        r = 0
        newx = (minx,midx)
    else:
        r = 1
        newx = (midx,maxx)
    if y < midy:
        s = 0
        newy = (miny,midy)
    else:
        s = 1
        newy = (midy,maxy)
    if z < midz:
        t = 0
        newz = (minz,midz)
    else:
        t = 1
        newz = (midz,maxz)

    return ((r,s,t), (newx, newy, newz))


def euclidean_point_point(p,q):
    "The euclidean distance between points p and q"
    (x1,y1,z1) = p
    (x2,y2,z2) = q
    return sqrt((x1-x2)**2 + (y1-y2)**2 + (z1-z2)**2)


def nearest_point_in_box(p,b):
    "Returns the nearest point in a box b to a point p"
    ((minx,maxx), (miny,maxy), (minz,maxz)) = b
    (x,y,z) = p
    if x<minx:
        x0 = minx
    elif x<maxx:
        x0 = x
    else:
        x0 = maxx
    if y<miny:
        y0 = miny
    elif y<maxy:
        y0 = y
    else:
        y0 = maxy
    if z<minz:
        z0 = minz
    elif z<maxz:
        z0 = z
    else:
        z0 = maxz
    return (x0,y0,z0)


def furthest_point_in_box(p,b):
    "Returns the furthest point in a box b to a point p"
    ((minx,maxx), (miny,maxy), (minz,maxz)) = b
    (x,y,z) = p
    if 2*x > minx+maxx:
        x0 = minx
    else:
        x0 = maxx
    if 2*y > miny+maxy:
        y0 = miny
    else:
        y0 = maxy
    if 2*z > minz+maxz:
        z0 = minz
    else:
        z0 = maxz
    return (x0,y0,z0)


def euclidean_point_box(p,b):
    "The euclidean distance between p and a box b"
    return euclidean_point_point(p,nearest_point_in_box(p,b))


def euclidean_point_box_max(p,b):
    "The furthest distance between p and a box b"
    return euclidean_point_point(p,furthest_point_in_box(p,b))


def euclidean_box_box(b1,b2):
    "The euclidean distance between two boxes"
    ((minx1,maxx1), (miny1,maxy1), (minz1,maxz1)) = b1
    ((minx2,maxx2), (miny2,maxy2), (minz2,maxz2)) = b2
    if maxx1 < minx2:
        x = minx2 - maxx1
    elif maxx2 < minx1:
        x = minx1 - maxx2
    else:
        x = 0
    if maxy1 < miny2:
        y = miny2 - maxy1
    elif maxy2 < miny1:
        y = miny1 - maxy2
    else:
        y = 0
    if maxz1 < minz2:
        z = minz2 - maxz1
    elif maxz2 < minz1:
        z = minz1 - maxz2
    else:
        z = 0
    return sqrt(x*x+y*y+z*z)


def euclidean_box_box_max(b1,b2):
    "The maximum distance between two boxes"
    ((minx1,maxx1), (miny1,maxy1), (minz1,maxz1)) = b1
    ((minx2,maxx2), (miny2,maxy2), (minz2,maxz2)) = b2
    x = max(maxx2-minx1,maxx1-minx2)
    y = max(maxy2-miny1,maxy1-miny2)
    z = max(maxz2-minz1,maxz1-minz2)
    return sqrt(x*x+y*y+z*z)


def euclidean_box_box_minmax(b1,b2):
    """
    The minimum over all points in b1 of the maximum over all points
    in b2 of the distance.
    """
    ((minx1,maxx1), (miny1,maxy1), (minz1,maxz1)) = b1
    ((minx2,maxx2), (miny2,maxy2), (minz2,maxz2)) = b2
    x = min(max(abs(minx2-minx1),abs(maxx2-minx1)),max(abs(minx2-maxx1),abs(maxx2-maxx1)))
    y = min(max(abs(miny2-miny1),abs(maxy2-miny1)),max(abs(miny2-maxy1),abs(maxy2-maxy1)))
    z = min(max(abs(minz2-minz1),abs(maxz2-minz1)),max(abs(minz2-maxz1),abs(maxz2-maxz1)))
    return sqrt(x*x+y*y+z*z)
    

def convex_box_deform(f,b):
    """
    Given a function f taking points to points, and a box b, returns
    the box containing f applied to the vertices of b.
    """
    l = [f(p) for p in vertices(b)]
    minx = min(q[0] for q in l)
    maxx = max(q[0] for q in l)
    miny = min(q[1] for q in l)
    maxy = max(q[1] for q in l)
    minz = min(q[2] for q in l)
    maxz = max(q[2] for q in l)
    return ((minx,maxx),(miny,maxy),(minz,maxz))


def matrix_action(m,p):
    return tuple(sum(m[i][j]*p[j] for j in xrange(3)) for i in xrange(3))
