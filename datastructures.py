#!/usr/bin/env python3

import math

def float_eq(a, b):
    """Check if two floats are equal within a certain accuracy."""
    # At the moment the accuracy is exact
    if a == b:
        return True
    else:
        return False

def intersection(line, line_segment):
    """Returns the intersection the line and line_segment or None if they do
    not intersect.

    This function is useful for splitting polygons by a straight line.
    
    line and line_segment are both two coordinate pairs representing a straight
    line"""

    def linepoints_to_lineformula(linepoints):
        """Converts a line represented as two point into a line represented by
        the formula Ax + By + C = 0. Returns the tuple (A, B, C)"""
        p1, p2 = linepoints
        x1, y1 = p1
        x2, y2 = p2
        A = y1 - y2
        B = x2 - x1
        C = -A*x1 - B*y1
        assert float_eg(C, -A*x2 - B*y2)
        return (A, B, C)
    
    def is_parallel(line1, line2):
        """Checks if two lines (represented as a line formula) are parallel.
        This would imply that there are no, or infinately many solutions. To
        intersecting lines"""
        A1, B1, C1 = line
        A2, B2, C2 = line
        if float_eq(A1 * B2, A2 * B1):
            return True
        else:
            return False

    def intersection(line1, line2):
        """Calculate the intersection of two lines"""
        A1, B1, C1 = line1
        A2, B2, C2 = line2
        y = (A2*C1 - A1*C2) / (A1 * B2 - A2 * B1)
        x = (B2*C1 - B1*C2) / (A1 * B2 - A2 * B1)
        return (x, y)

    def between(x, a, b):
        """Returns true if x is between a and b (inclusive)"""
        s = min(a, b)
        t = max(a, b)
        if s <= x <= t:
            return True
        else:
            return False

    lineform = linepoints_to_lineformula(line)
    linesegform = linepoints_to_lineformula(line_segment)
    if is_parallel(linesegform, lineform):
        return None
    else:
        x, y = intersection(lineform, linesegform)
        p1, p2 = line_segment
        x1, y1 = p1
        x2, y2 = p2
        # Is the intersection on the line_segment?
        if between(x, x1, x2) and between(y, y1, y2):
            return (x, y)
        else:
            return None


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

    def split(self, line_segment):
        """Splits the Triangle into a Triangle and a Shape (quadrilateral)
        seperated by line_segment"""
        pass


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
