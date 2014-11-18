#!/usr/bin/env python3

from tkinter import *
from tkinter import ttk

PHI = (1 + 5**0.5) / 2
canvas_height = 400

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

def step_forward():
    """Draws the next step in turing polygon into a square"""

def step_backwards():
    """Draws the previous step in turing polygon into a square"""

def clear_canvas():
    """Deletes the current polygon from the canvas."""
    global points
    # Delete all points
    points = list()
    # Clear lines and points from the canvas
    canvas.delete('line', 'point')


def squarify_polygon(*args):
    """Turns the polygon into a square"""
    print('Squarify')

def jump_to_position(pos):
    """Jump to the position (-1 for final position)"""
    print('Jump to: ' +  str(pos))

root = Tk()

mainframe = ttk.Frame(root)
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

canvas = Canvas(mainframe, width=canvas_height, height=canvas_height)
canvas.bind('<Button-1>', add_point)
canvas.grid(column=1, row=0, sticky=(N, W, E, S))

buttonframe = ttk.Frame(mainframe)
buttonframe.grid(column=0, row=0, sticky=(N, W, E, S))

squarify = ttk.Button(buttonframe, text='Squarify polygon', command = squarify_polygon)
squarify.grid(column=0, row=0, sticky=(N, W, E))

clear = ttk.Button(buttonframe, text='Clear', command = clear_canvas)
clear.grid(column=0, row=1, sticky=(N, W, E))

controlsframe = ttk.Frame(buttonframe)
controlsframe.grid(column=0, row=2, sticky = (W, E))

start = ttk.Button(controlsframe, text='<<', command = lambda x : jump_to_position(0), width=2)
start.state(['disabled'])
start.grid(column=0, row=0, sticky = (N, S, W, E))

stepback = ttk.Button(controlsframe, text='|<', command = step_backwards, width=2)
stepback.state(['disabled'])
stepback.grid(column=1, row=0, sticky = (N, S, W, E))

position = StringVar()
position.set('0')
poslabel = ttk.Entry(controlsframe, textvariable=position, width=3)
poslabel.state(['disabled'])
poslabel.bind('<Return>', lambda x : jump_to_position(int(position.get())))
poslabel.grid(column=2, row = 0,  sticky = (N, S, W, E))

stepforward = ttk.Button(controlsframe, text='>|', command = step_forward, width=2)
stepforward.state(['disabled'])
stepforward.grid(column=3, row=0, sticky = (W, E, N, S))

start = ttk.Button(controlsframe, text='>>', command = lambda x : jump_to_position(-1), width=2)
start.state(['disabled'])
start.grid(column=4, row=0, sticky = (N, S, W, E))

root.mainloop()
