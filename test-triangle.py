#!/usr/bin/env python3

from tkinter import *
from tkinter import ttk
from datastructures import Triangle
import math

PHI = (1 + 5**0.5) / 2
canvas_height = 300

# A temporary list of points the user placed on the canvas
points = list()
# A dictionary of triangles
triangles = dict()
# pivot to rotate around
global_pivot = None

def add_point(event):
    """Adds a point to the canvas. If there are three loose points, they will
    be connected to form a triangle."""
    ex, ey = event.x, event.y
    points.append((ex, ey))
    i = canvas.create_oval((ex - 2, ey - 2, ex + 2, ey + 2))
    canvas.addtag('point', 'withtag', i)
    while len(points) >= 3:
        p1, p2, p3 = points.pop(), points.pop(), points.pop()
        triangles
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
        ni = canvas.create_polygon(new_tri.points)
        canvas.addtag('triangle', 'withtag', ni)
        canvas.tag_bind(ni, '<Button-1>', rotate_triangle(ni))
        triangles[ni] = new_tri
    return rotate_tri

def clear_canvas():
    global points, triangles, global_pivot
    points = list()
    triangles = dict()
    global_pivot = None
    canvas.delete('triangle', 'point')

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
frame.grid()
canvas.grid()
rotate.grid()
rotate_label.grid()
clear.grid()
root.mainloop()

