#!/usr/bin/env python3

from tkinter import *
from tkinter import ttk
from geometry import *
from random import randint
from collections import defaultdict
import math

PHI = (1 + 5**0.5) / 2
canvas_height = 300
TRIANGLE_MODE = 0
LINE_MODE = 1
mode = TRIANGLE_MODE

# A temporary list of points the user placed on the canvas
points = list()
# A dictionary of triangles
triangles = dict()
def random_color():
    color = randint(0, 0xFFFFFF)
    return hex_color(color)

# A dictionary that colors the triangle
colors = defaultdict(random_color)
# pivot to rotate around
global_pivot = None

def hex_color(color):
    return '#' + hex(color)[2:].rjust(6, '0')

def draw_shape(shape):
    global color, color_inc
    tris = shape.triangles
    for t in tris:
        i = canvas.create_polygon(t.points, fill=colors[t])
        canvas.addtag('triangle', 'withtag', i)
        canvas.tag_bind(i, '<Button-1>', rotate_triangle(i))
        triangles[i] = t


def add_point(event):
    """Adds a point to the canvas. If there are three loose points, they will
    be connected to form a triangle."""
    global mode, triangles
    ex, ey = event.x, event.y
    points.append((ex, ey))
    i = canvas.create_oval((ex - 2, ey - 2, ex + 2, ey + 2))
    canvas.addtag('point', 'withtag', i)
    if mode == LINE_MODE and len(points) >= 2:
        p1, p2 = points.pop(), points.pop()
        x1, y1 = p1
        x2, y2 = p2
        i = canvas.create_line((x1, y1, x2, y2))
        canvas.addtag('line', 'withtag', i)
        new_shapes = list()
        for t in triangles.values():
            u, d = t.split(LineSegment(p1, p2).to_line())
            new_shapes.append(u)
            new_shapes.append(d)
        canvas.delete('triangle')
        triangles = dict()
        for s in new_shapes:
            draw_shape(s)
        mode = TRIANGLE_MODE
    while len(points) >= 3 and mode == TRIANGLE_MODE:
        p1, p2, p3 = points.pop(), points.pop(), points.pop()
        i = canvas.create_polygon((p1, p2, p3))
        canvas.addtag('triangle', 'withtag', i)
        canvas.tag_bind(i, '<Button-1>', rotate_triangle(i))
        triangles[i] = Triangle((p1, p2, p3))

def set_pivot(event):
    global global_pivot
    global_pivot = (event.x, event.y)

def update_rotate(x):
    rotate_display.set(x)

def rotate_triangle(i):
    def rotate_tri(event):
        new_tri = triangles[i].rotate(global_pivot, rotate.get() * math.pi / 180)
        print(rotate.get() * math.pi / 180)
        del triangles[i]
        canvas.delete(i)
        ni = canvas.create_polygon(new_tri.points, fill=colors[new_tri])
        canvas.addtag('triangle', 'withtag', ni)
        canvas.tag_bind(ni, '<Button-1>', rotate_triangle(ni))
        triangles[ni] = new_tri
    return rotate_tri

def clear_canvas():
    global points, triangles, global_pivot
    points = list()
    triangles = dict()
    global_pivot = None
    canvas.delete('triangle', 'point', 'line')

def set_state_line():
    global mode
    mode = LINE_MODE

root = Tk()
frame = ttk.Frame(root)
canvas = Canvas(frame, width=canvas_height*PHI, height=canvas_height)
canvas.bind('<Button-1>', add_point)
canvas.bind('<Button-3>', set_pivot)
rotate = ttk.Scale(frame, length=200, from_=-360, to=360, orient=HORIZONTAL,
        command=update_rotate)
rotate_label = ttk.Label(frame, text=rotate.get())
rotate_display =  StringVar()
rotate_label['textvariable'] = rotate_display
clear = ttk.Button(frame, text='Clear', command = clear_canvas)
cutLine = ttk.Button(frame, text='Cut By Line', command = set_state_line)

frame.grid()
canvas.grid()
rotate.grid()
rotate_label.grid()
clear.grid()
cutLine.grid()
root.mainloop()
