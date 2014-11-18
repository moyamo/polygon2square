#!/usr/bin/env python3

import math
from functools import cmp_to_key, partial

def float_eq(a, b):
    """Check if two floats are equal within a certain accuracy."""
    epsilon = 2**(-10)
    return abs(a - b) < epsilon

def point_eq(a, b):
    """Check if two points are equal within a certain accuracy."""
    return float_eq(a[0], b[0]) and float_eq(a[1], b[1])

def point_cmp(a, b):
    """Check if two points are equal, less than or greater than within a
    certain accuracy."""
    if point_eq(a, b):
        return 0
    elif float_eq(a[0], b[0]) and a[1] < b[1]:
        return -1
    elif float_eq(a[0], b[0]) and a[1] > b[1]:
        return 1
    elif a < b:
        return -1
    else:
        return 1

def clockwise_from(p0, p1, p2):
    """Returns a value > 0 if p1 is clockwise of p2 from p0, < 0 if counter
    clockwise and == 0 if collinear"""
    x1, y1 = p1[0] - p0[0], p1[1] - p0[1]
    x2, y2 = p2[0] - p0[0], p2[1] - p0[1]
    ans = x1*y2 - x2*y1
    if float_eq(ans, 0):
        return 0
    elif ans < 0:
        return -1
    else:
        return 1


def clockwise_and_dist(p0, p1, p2):
    """Returns a value > 0 if p1 is clockwise of p2 from p0, < 0 if counter
    clockwise, if the points are collinear it will return 1 if p2 is further
    from p0 than p1 and -1 if p2 is closer to p0 than p1"""
    a = clockwise_from(p0, p1, p2)
    if a == 0:
        dist1 = LineSegment(p0, p1).length()
        dist2 = LineSegment(p0, p2).length()
        if float_eq(dist1, dist2):
            return 0
        elif dist1 < dist2:
            return -1
        else:
            return 1
    else:
        return a
        


def line_intersects_segment(line, line_segment):
    """Returns the intersection the Line and LineSegment or None if they do
    not intersect.

    This function is useful for splitting polygons by a straight line.
    """

    linesegform = line_segment.to_line()
    if line.is_parallel_to(linesegform):
        return None
    else:
        p = line.intersection(linesegform)
        # Is the intersection on the line_segment?
        if line_segment.between(p):
            return p
        else:
            return None

class LineSegment:
    """A straight line bounded by two points.

    LineSegment represents a straight line that is bounded by two points.
    The datastructure should be considered immutable.
    """
    def __init__(self, point1, point2):
        """point1 and point2 represent the two bounding points of the segment
        """
        self.points = (point1, point2)

    def __repr__(self):
        return repr(self.points)

    def length(self):
        x1, y1 = self.points[0]
        x2, y2 = self.points[1]
        return math.hypot(x1 - x2, y1 - y2)

    def midpoint(self):
        """Return midpoint of LineSegment"""
        x1, y1 = self.points[0]
        x2, y2 = self.points[1]
        return ((x1 + x2) / 2, (y1 + y2) / 2)

    def point_by_length(self, length):
        """Return a point on the ray points[0] to points[1]  such that the
        distance from points[0] to the new point is 'length'"""
        r = self.length()
        d = length
        x1, y1 = self.points[0]
        x2, y2 = self.points[1]
        x3 = (x2 - x1) * d / r + x1
        y3 = (y2 - y1) * d / r + y1
        return (x3, y3)

    def to_line(self):
        """Converts this LineSegment into a Line (by extending both ends)

        Returns a Line
        """
        p1, p2 = self.points
        x1, y1 = p1
        x2, y2 = p2
        A = y1 - y2
        B = x2 - x1
        C = -A*x1 - B*y1
        assert float_eq(C, -A*x2 - B*y2)
        line = Line(A, B, C)
        return line
    
    def between(self, point):
        """Return True if point is between the LineSegment.
        
        A point is between a line segment if it is between the x and y values
        that bound the segment. The point need not lie on the segment.
        To check if a point lies on a LineSegment use to_line and
        Line.side_of_line
        """
        def btw(x, a, b):
            """Returns true if x is between a and b (inclusive)"""
            s = min(a, b)
            t = max(a, b)
            return (s <= x or float_eq(s, x)) and (x <= t or float_eq(x, t))

        x, y = point
        x1, y1 = self.points[0]
        x2, y2 = self.points[1]
        return btw(x, x1, x2) and btw(y, y1, y2)
    
class Line:
    """A straight line
    
    Represents a straight line as (A, B, C) where Ax + By + C = 0.
    The line is not normalised (I haven't found an elegant way to do this)

    Should be treated as an immutable data structure. However it is not
    internally so, and utilises caching.
    """
    def __init__(self, A, B, C):
        """Ax + By + C = 0 and A + B + C = 1 """
        self.A = A 
        self.B = B
        self.C = C

    def side_of_line(self, point):
        """Returns the number 1, 0, -1 if point is on the positive side, on the
        line, on the negative side of the line respectively."""

        A, B, C = self.A, self.B, self.C
        x, y = point
        value = A * x + B * y + C
        if float_eq(value, 0):
            return 0
        elif value > 0:
            return 1
        elif value < 0:
            return -1

    def is_parallel_to(self, line2):
        """Checks if this lines is parallel to line2. """
        A1, B1, C1 = self.A, self.B, self.C
        A2, B2, C2 = line2.A, line2.B, line2.C
        if float_eq(A1 * B2, A2 * B1):
            return True
        else:
            return False

    def intersection(self, line2):
        """Calculate the intersection of this line with line2"""
        A1, B1, C1 = self.A, self.B, self.C
        A2, B2, C2 = line2.A, line2.B, line2.C
        y = (A2*C1 - A1*C2) / (A1 * B2 - A2 * B1)
        x = (B1*C2 - B2*C1) / (A1 * B2 - A2 * B1)
        return (x, y)

    def perpendicular(self, point):
        """Return a line perpendicular to this one passing through point"""
        x, y = point
        A = -self.B
        B = self.A
        C = -A*x - B*y
        return Line(A, B, C)

    def parallel(self, point):
        """Return a line parallel to this one passing through point"""
        x, y = point
        A = self.A
        B = self.B
        C = -A*x - B*y
        return Line(A, B, C)
    
    def __repr__(self):
        return '(' + ', '.join(str(s) for s in [self.A, self.B, self.C]) + ')'


class Triangle:
    """A class structure for storing and minipulating a triangle.

    The trianlge is represented as a 3-tuple of points. Each point is
    represented as a 2-tuple of floats, the first element being the
    x-coordinate and the second element being the y-coordinate.

    Several useful operations can be applied to a triangle such as, rotate,
    translate, split across altitude, and rectanglify.

    The Triangle (and underlying tuple) should be treated as an immutable
    data structure. All methods return a new triangle and do not modify the
    existing one."""

    def __init__(self, tpl):
        """tpl is a 3-tuple of coordinates"""
        self.points = tpl

    def __iter__(self):
        """Returns the tuple of points"""
        return iter(self.points)

    @property
    def segments(self):
        """A list of segments representing the sides of the line.
        
        The ith line will be opposite the ith point
        """
        return [LineSegment(self.points[1], self.points[2]),
                LineSegment(self.points[0], self.points[2]),
                LineSegment(self.points[0], self.points[1])
                ]

    def angle(self, i):
        """Return the angle at the ith point"""
        segs = self.segments
        a = segs[i].length()
        b = segs[(i + 1) % 3].length()
        c = segs[(i + 2) % 3].length()
        thing = (a**2 - b**2 - c**2)/(-2*b*c)
        # Get rid of rounding errors for boundry values
        if float_eq(thing, -1):
            thing = -1
        elif float_eq(thing, 1):
            thing = 1
        return math.acos(thing)
    
    def largest_angle(self):
        """Return the the number of the point at the largest angle"""
        cur_max = 0
        big_ang = None
        for i in range(len(self.points)):
            ang = self.angle(i)
            if ang > cur_max:
                cur_max = ang
                big_ang = i
        return big_ang
    
    def rotate(self, pivot, rangle):
        """Return a new triangle rotate clockwise (by angle) around pivot.
        
        pivot -- A coordinate pair
        rangle -- The angle to rotate by in radians"""
        new_points = list()
        px, py = pivot
        for x, y in self.points:
            dx, dy = x - px, y - py
            current_angle = math.atan2(dy, dx)
            total_angle = current_angle - rangle
            r = math.hypot(dx, dy)
            nx = r*math.cos(total_angle) + px
            ny = r*math.sin(total_angle) + py
            new_points.append((nx, ny))
        return Triangle(tuple(new_points))

    def translate(self, translation):
        """Return a new triangle translated by 'translation'"""
        tx, ty = translation
        new_points = [(x + tx, y + ty) for x, y in self.points]
        return Triangle(tuple(new_points))

    def to_rightangle(self):
        """Splits the triangle into two right-angled triangles"""
        # We need to cut the triangle across the largest angle (in case it's
        # obtuse)
        p = self.points
        big_point = self.largest_angle()
        other_points = [(big_point + 1) % 3, (big_point + 2) % 3]
        cut = self.segments[big_point].to_line().perpendicular(p[big_point])
        new_point = line_intersects_segment(cut, self.segments[big_point])
        t1 =  Triangle((p[big_point], new_point, p[other_points[0]]))
        t2 =  Triangle((p[big_point], new_point, p[other_points[1]]))
        return (t1, t2)
        
    def to_rectangle(self):
        """Turns a right angle triangle into a rectangle (Shape)"""
        p = self.points
        # The point at right angle
        right = self.largest_angle()
        assert float_eq(self.angle(right), math.pi / 2)
        other = [(right + 1) % 3, (right + 2) % 3]
        hyp = self.segments[right]
        base = self.segments[other[0]]
        height = self.segments[other[1]]
        # We will cut the triangle at the midpoint of the height
        midp = height.midpoint()
        rect_side = base.to_line().parallel(midp)
        other_point = line_intersects_segment(rect_side, hyp)
        t1 = Triangle((p[other[0]], midp, other_point)).rotate(other_point, math.pi)
        t2 = Triangle((p[right], p[other[1]], midp))
        t3 = Triangle((p[other[1]], midp, other_point))
        return Shape([t1, t2, t3])
        
    def split(self, line):
        """Splits the Triangle into two shapes separated by line.

        All the points of the first shape will be on the non-negative side of
        line. All the points of the second shape will be on the non-positive
        side of the line.
        """
        sides = [line.side_of_line(p) for p in self.points]

        # The whole triangle is on the same side of the line
        if sides[0] == sides[1] == sides[2]:
            if sides[0] == 1:
                return (Shape([self]), Shape([]))
            else:
                return (Shape([]), Shape([self]))

        # The triangle is cut into two, on one vertex
        elif sorted(sides) == [-1, 0, 1]:
            inverse = [None for i in range(3)]
            for i, s in enumerate(sides):
                inverse[s % 3] = self.points[i]
            base = LineSegment(inverse[1], inverse[2])
            basepoint = line_intersects_segment(line, base)
            pos_shape = Triangle((basepoint, inverse[0], inverse[1]))
            neg_shape = Triangle((basepoint, inverse[0], inverse[2]))
            return (Shape([pos_shape]), Shape([neg_shape]))

        # Line is "tangent" to triangle
        elif 0 in sides:
            if 1 in sides:
                return (Shape([self]), Shape([]))
            elif -1 in sides:
                return (Shape([]), Shape([self]))

        # Line intersects two segments
        else:
            segs = self.segments
            intersects = (line_intersects_segment(line, s) for s in segs)
            intersects = [i for i in intersects if i != None]
            assert len(intersects) == 2
            sided_points = [[], []]
            for i, s in enumerate(sides):
                if s == 1:
                    sided_points[1].append(self.points[i])
                elif s == -1:
                    sided_points[0].append(self.points[i])
            if len(sided_points[0]) == 1:
                t1 = Triangle((sided_points[0][0], intersects[0], intersects[1]))
                t2 = Triangle((sided_points[1][0], intersects[0], intersects[1]))
                t3 = Triangle((sided_points[1][0], sided_points[1][1], intersects[0]))
                return (Shape([t2, t3]), Shape([t1]))
            elif len(sided_points[1]) == 1:
                t1 = Triangle((sided_points[1][0], intersects[0], intersects[1]))
                t2 = Triangle((sided_points[0][0], intersects[0], intersects[1]))
                t3 = Triangle((sided_points[0][0], sided_points[0][1], intersects[0]))
                return (Shape([t1]), Shape([t2, t3]))
            else:
                raise Exception("Segments missing")

class Shape:
    """A class structure for representing and minipulating arbitary shapes.
    
    A shape is defines as a list of triangles (see Triangle). Several
    operations can be applied to a shape such as rotation, translation and
    splitting the shape into two.

    This object should be treated as an immutable data structure. All methods
    return new shapes and do not modify the existing one."""

    def __init__(self, triangle_list):
        """triangle_list is a list of triangles"""
        self.triangles = triangle_list
        self._convex_hull = None
    
    def split(self, line):
        """Splits the Shape into two shapes separated by line.

        All the points of the first shape will be on the non-negative side of
        line. All the points of the second shape will be on the non-positive
        side of the line.
        """
        up = list()
        down = list()
        for t in self.triangles:
            u, d = t.split(line)
            up.extend(u.triangles)
            down.extend(d.triangles)
        return (Shape(up), Shape(down))

    def translate(self, translation):
        """Return a new Shape translated by 'translation'"""
        return Shape([t.translate(translation) for t in self.triangles])

    def rotate(self, pivot, rangle):
        """Return a new Shape rotate clockwise (by angle) around pivot."""
        return Shape([t.rotate(pivot, rangle) for t in self.triangles])
    
    def vertices(self):
        """Return vertices inside this shape."""
        vertices = list()
        for t in self.triangles:
            vertices.extend(t.points)
        undup = list()
        for v in vertices:
            for u in undup:
                if point_eq(u, v):
                    break
            else:
                undup.append(v)
        return undup
    
    def convex_hull(self):
        """Return the convex hull of the shape.
        
        This uses grahams algorithm [O(V log V)] and caches the result inside
        self._convex_hull .
        """
        verts = self.vertices()
        if len(verts) == 0:
            self._convex_hull = []
        elif self._convex_hull is None:
            p = min(verts, key=cmp_to_key(point_cmp))
            verts.remove(p)
            ps = sorted(verts, key=cmp_to_key(partial(clockwise_and_dist, p)))
            ps.append(p)
            hull = [p, ps[0]]
            i = 1
            while clockwise_from(hull[0], hull[1], ps[i]) >= 0:
                hull.pop()
                hull.append(ps[i])
                i += 1
            hull.append(ps[i])
            for l in ps[i:]:
                while clockwise_from(hull[-2], hull[-1], l) >= 0:
                    hull.pop()
                hull.append(l)
            hull.pop()
            self._convex_hull = hull
        return self._convex_hull

    def height(self):
        """Return the height of the rectangle"""
        a, b, c, d = self.convex_hull()
        s1 = LineSegment(a, b)
        s2 = LineSegment(b, c)
        height = s2 if s1.length() < s2.length() else s1
        return height

    def width(self):
        """Return the width of the rectangle"""
        a, b, c, d = self.convex_hull()
        s1 = LineSegment(a, b)
        s2 = LineSegment(b, c)
        width = s1 if s1.length() < s2.length() else s2
        return width

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
            return Shape(rec1.triangles + rec2.triangles).squish_rectangle()
        else:
            return self

    def square_rectangle(self):
        """Return a square of equal area to the rectangle. """
        rect = self.squish_rectangle()
        a, b, c, d = rect.convex_hull()
        s1 = LineSegment(a, b)
        s2 = LineSegment(b, c)
        if float_eq(s1.length(), s2.length()):
            return self
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

        for p in triangle.convex_hull():
            if not point_eq(p, b) and not point_eq(p, c):
                anchor = p

        tri_trans = (corner2[0] - anchor[0], corner2[1] - anchor[1])
        triangle = triangle.translate(tri_trans)
        otri_trans = (anchor[0] - b[0], anchor[1] - b[1])
        other_triangle = other_triangle.translate(otri_trans)
        return Shape(rest.triangles + triangle.triangles + other_triangle.triangles)

    def orientate(self):
        """Rotates the shape so that the first segment in the convex hull is
        parralell to the x-axis."""
        hull = self.convex_hull()
        x1, y1 = hull[0]
        x2, y2 = hull[1]
        xd, yd = x1 - x2, y1 - y2
        return self.rotate(hull[1], math.atan2(yd, xd))
