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
            except StopIteration:
                raise IndexError('FrameList index out of bounds')
            self._cache.append(f)
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
        yield last
        new_last = list()
        while len(last) > 0:
            t = last.pop()
            new_last.extend(t.to_rightangle())
            yield new_last + last
        last, new_last = new_last, list()
        while len(last) > 0:
            t = last.pop()
            new_last.append(t.to_rectangle())
            yield new_last + last
        last, new_last = new_last, list()
        while len(last) > 0:
            s = last.pop()
            new_last.append(s.square_rectangle())
            yield new_last + last

        last, new_last = new_last, list()
        while len(last) > 1:
            r, s = last.pop(), last.pop()
            q = s.merge_square(r)
            p = q.convex_hull()[0]
            t = (50 - p[0], 50 - p[1])
            last.append(q.translate(t))
            yield last
