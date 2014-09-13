#!/usr/bin/env python3

from tkinter import *
from tkinter import ttk

PHI = (1 + 5**0.5) / 2
canvas_height = 300

# A list of points the user placed on the canvas
points = list()
last_line = None

def add_point(event):
    """Adds a point to the 'points' list and draw it on the canvas"""
    global last_line
    ex, ey = event.x, event.y

    # Create the point
    points.append((ex, ey))
    i = canvas.create_oval((ex - 2, ey - 2, ex + 2, ey + 2))
    canvas.addtag('point', 'withtag', i)

    # Connect lines to the point
    if len(points) > 1:
        x1, y1 = points[-1]
        x2, y2 = points[-2]
        i = canvas.create_line((x1, y1, x2, y2))
        canvas.addtag('line', 'withtag',  i)

    # If we have enough points to create a polygon, connect the last point
    # with the first point.
    if len(points) > 2:
        x1, y1 = points[-1]
        x2, y2 = points[0]
        if last_line != None:
            canvas.delete(last_line)
        last_line = canvas.create_line((x1, y1, x2, y2))
        canvas.addtag('line', 'withtag', last_line)

def clear_canvas():
    """Deletes the current polygon from the canvas."""
    global points
    # Delete all points
    points = list()
    # Clear lines and points from the canvas
    canvas.delete('line', 'point')


def squarify_polygon():
    pass

root = Tk()
frame = ttk.Frame(root)
canvas = Canvas(frame, width=canvas_height*PHI, height=canvas_height)
canvas.bind('<Button-1>', add_point)
squarify = ttk.Button(frame, text='Squarify polygon', command = squarify_polygon)
clear = ttk.Button(frame, text='Clear', command = clear_canvas)
frame.grid()
canvas.grid()
squarify.grid()
clear.grid()
root.mainloop()

