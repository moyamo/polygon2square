#!/usr/bin/env python3

from tkinter import *
from tkinter import ttk

PHI = (1 + 5**0.5) / 2
canvas_height = 300

def squarify_polygon():
    pass

root = Tk()
frame = ttk.Frame(root)
canvas = Canvas(frame, width=canvas_height*PHI, height=canvas_height)
squarify = ttk.Button(frame, text='Squarify polygon', command = squarify_polygon)
frame.grid()
canvas.grid()
squarify.grid()
root.mainloop()

