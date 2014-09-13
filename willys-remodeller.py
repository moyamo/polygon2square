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

    # Create the point
    points.append((event.x, event.y))
    i = canvas.create_oval((event.x - 2, event.y - 2, event.x + 2, event.y + 2))
    canvas.addtag('point', 'withtag', i)

    # Connect lines to the point
    if len(points) > 1:
        point1 = points[-1]
        point2 = points[-2]
        i = canvas.create_line((point1[0], point1[1], point2[0], point2[1]))
        canvas.addtag('line', 'withtag',  i)
    if len(points) >= 3:
        point1 = points[-1]
        point2 = points[0]
        if last_line != None:
            canvas.delete(last_line)
        last_line = canvas.create_line((point1[0], point1[1], point2[0], point2[1]))
        canvas.addtag('line', 'withtag', last_line)
    print(event.x, event.y)

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

