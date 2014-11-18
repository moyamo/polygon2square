#!/usr/bin/env python3

from geometry import *

class FrameList:
    """Acts like a lazy list that contains a snapshot of every step needed to
    square the polygon.
    
    The frame contains a generator that generates every step of the polygon,
    and a list that contains everystep generated so far.
    """
    
    def __init__(self, polygon):
        """Creates a FrameList for polygon"""
        self._polygon = polygon
        self._generator = self._squarify()
        self._cache = list()

    def __getitem__(self, i):
        """Returns the ith Frame"""
        while len(self._cache) <= i:
            try:
                f = next(self._generator)
                self._cache.append(f)
            except StopIteration:
                raise IndexError('FrameList index out of bounds')
        print(self._cache[i])
        return self._cache[i]

    def _polygon2triangles(self):
        """Takes a list of points (polygon) and returns a list of Triangles
        created by diagonalizing the polygon"""
        polygon = self._polygon
        common_point = polygon[0]
        return [Triangle((common_point, p, q))
                for p, q in zip(polygon[1:], polygon[2:])]

    def _squarify(self):
        """"A generator function that returns frames of converting a polygon
        to a square"""
        last = self._polygon2triangles()
        yield last[:]
        new_last = list()
        # Turn all triangles to right-angled triangles
        while len(last) > 0:
            t = last.pop()
            new_last.extend(t.to_rightangle())
            yield new_last + last

        # Turn all right-angled triangles to rectangles
        last, new_last = new_last, list()
        while len(last) > 0:
            t = last.pop()
            new_last.append(None)
            for t in triangle2rectangle(t):
                a = new_last.pop()
                new_last.append(t)
                yield new_last + last

        # Turn all rectangles to squares
        last, new_last = new_last, list()
        while len(last) > 0:
            s = last.pop()
            new_last.append(None)
            for r in rectangle2square(s):
                new_last.pop()
                new_last.append(r)
                yield new_last + last

        # Merge all squares
        last, new_last = new_last, list()
        while len(last) > 1:
            r, s = last.pop(), last.pop()
            q = s.merge_square(r)
            p = q.convex_hull()[0]
            t = (50 - p[0], 50 - p[1])
            last.append(q.translate(t))
            yield last[:]

def triangle2rectangle(tri):
    """Turns a right angle triangle into a rectangle (Shape).
    
    This function is a generator function that generates a Shape for every step
    needed to turn the triangle into a rectangle.
    """
    p = tri.points
    # The point at right angle
    right = tri.largest_angle()
    assert float_eq(tri.angle(right), math.pi / 2)
    other = [(right + 1) % 3, (right + 2) % 3]
    hyp = tri.segments[right]
    base = tri.segments[other[0]]
    height = tri.segments[other[1]]
    # We will cut the triangle at the midpoint of the height
    midp = height.midpoint()
    rect_side = base.to_line().parallel(midp)
    other_point = line_intersects_segment(rect_side, hyp)
    t1 = Triangle((p[other[0]], midp, other_point))
    t2 = Triangle((p[right], p[other[1]], midp))
    t3 = Triangle((p[other[1]], midp, other_point))
    yield Shape([t1, t2, t3])
    t1 = t1.rotate(other_point, math.pi)
    yield Shape([t1, t2, t3])

def squish_rectangle(self):
    """Return a rectangle of equal area such that height / width < 2"""
    a, b, c, d = self.convex_hull()
    s1 = LineSegment(a, b)
    s2 = LineSegment(b, c)
    width = s1 if s1.length() < s2.length() else s2
    height = s2 if s1.length() < s2.length() else s1
    if height.length() > 2 * width.length():
        midp = height.midpoint()
        cut = height.to_line().perpendicular(midp)
        rec1, rec2 = self.split(cut)
        yield Shape(rec1.triangles + rec2.triangles)
        h1 = rec1.convex_hull()
        h2 = rec2.convex_hull()
        common = None
        for p in h1:
            for q in h2:
                if float_eq(p[0], q[0]) and float_eq(p[1], q[1]):
                    common = q
                    break
            else:
                continue
            break
        rec1 = rec1.rotate(common, math.pi)
        s = Shape(rec1.triangles + rec2.triangles)
        yield s
        for t in squish_rectangle(s):
            yield t
    else:
        yield self


def rectangle2square(rectangle):
    """Return a square of equal area to the rectangle. """
    rect = squish_rectangle(rectangle)
    last = None
    for t in rect:
        if last is not None:
            yield last
        last = t
    rect = last
    a, b, c, d = rect.convex_hull()
    s1 = LineSegment(a, b)
    s2 = LineSegment(b, c)
    if float_eq(s1.length(), s2.length()):
        yield self
    elif s1.length() < s2.length():
        # Ensure s1 is height and s2 is width
        a, b, c, d = b, c, d, a
    s1 = LineSegment(a, b)
    s2 = LineSegment(b, c)
    s3 = LineSegment(c, d)
    s4 = LineSegment(d, a)
    revs4 = LineSegment(a, d)
    assert s1.length() > s2.length()
    square_side = (s1.length() * s2.length())**0.5
    corner1 = s1.point_by_length(square_side)
    corner2 = revs4.point_by_length(square_side)
    cut = LineSegment(b, corner2).to_line()
    r1, r2 = rect.split(cut)
    if len(r1.convex_hull()) == 3:
        triangle = r1
        rest = r2
    elif len(r2.convex_hull()) == 3:
        triangle = r2
        rest = r1
    else:
        raise Exception("Bad cut")

    yield Shape(triangle.triangles + rest.triangles)

    cut = s1.to_line().perpendicular(corner1)
    r1, r2 = rest.split(cut)
    if len(r1.convex_hull()) == 3:
        rest = r2
        other_triangle = r1
    elif len(r2.convex_hull()) == 3:
        rest = r1
        other_triangle = r2
    else:
        raise Exception("Bad cut")

    yield Shape(triangle.triangles + rest.triangles + other_triangle.triangles)

    for p in triangle.convex_hull():
        if not point_eq(p, b) and not point_eq(p, c):
            anchor = p

    tri_trans = (corner2[0] - anchor[0], corner2[1] - anchor[1])
    triangle = triangle.translate(tri_trans)
    yield Shape(triangle.triangles + rest.triangles + other_triangle.triangles)
    otri_trans = (anchor[0] - b[0], anchor[1] - b[1])
    other_triangle = other_triangle.translate(otri_trans)
    yield Shape(rest.triangles + triangle.triangles + other_triangle.triangles)
