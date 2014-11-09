#!/usr/bin/env python3

import math

def float_eq(a, b):
    """Check if two floats are equal within a certain accuracy."""
    epsilon = 2**(-30)
    if abs(a - b) < epsilon:
        return True
    else:
        return False

def line_intersects_segment(line, line_segment):
    """Returns the intersection the Line and LineSegment or None if they do
    not intersect.

    This function is useful for splitting polygons by a straight line.
    """

    def between(x, a, b):
        """Returns true if x is between a and b (inclusive)"""
        s = min(a, b)
        t = max(a, b)
        if s <= x <= t:
            return True
        else:
            return False

    linesegform = line_segment.to_line()
    if line.is_parallel_to(linesegform):
        return None
    else:
        x, y = line.intersection(linesegform)
        p1, p2 = line_segment.points
        x1, y1 = p1
        x2, y2 = p2
        # Is the intersection on the line_segment?
        if between(x, x1, x2) and between(y, y1, y2):
            return (x, y)
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
    
class Line:
    """A straight line
    
    Represents a straight line as (A, B, C) where Ax + By + C = 0 and
    A + B + C = 1.

    Should be treated as an immutable data structure.
    """
    def __init__(self, A, B, C):
        """Ax + By + C = 0 and A + B + C = 1

        NOTE: The constructor will ensure A + B + C = 1, the caller need not
        worry about homogenizing the coordinates.
        """
        sums = A + B + C
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

    @property
    def segments(self):
        """A list of segments representing the sides of the line."""
        return [LineSegment(self.points[0], self.points[1]),
                LineSegment(self.points[0], self.points[2]),
                LineSegment(self.points[1], self.points[2])
                ]


    def split(self, line):
        """Splits the Triangle into two shapes seperated by line.

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
            basepoint = line.intersection(inverse[1], inverse[2])
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
                t3 = Triangle((sided_points[1][0], sided_points[1][1], intersects[1]))
                return (Shape([t1]), Shape([t2, t3]))
            elif len(sided_points[1]) == 1:
                t1 = Triangle((sided_points[1][0], intersects[0], intersects[1]))
                t2 = Triangle((sided_points[0][0], intersects[0], intersects[1]))
                t3 = Triangle((sided_points[0][0], sided_points[0][1], intersects[1]))
                return (Shape([t2, t3]), Shape([t1]))
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
