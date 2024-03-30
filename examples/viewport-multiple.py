# -----------------------------------------------------------------------------
# Graphic Server Protocol (GSP)
# Copyright 2023 Vispy Development Team - BSD 2 Clauses licence
# -----------------------------------------------------------------------------
"""
# Simple light example

This example doesn't do much, it just makes a simple plot
"""
import matplotlib.pyplot as plt
from gsp.core import Canvas, Viewport

canvas = Canvas(512, 512, 100.0)
Viewport(canvas, 0, 0, 256, 256, (1,0,0,1))
Viewport(canvas, 0, 256, 256, 256, (0,1,0,1))
Viewport(canvas, 256, 0, 256, 256, (0,0,1,1))
Viewport(canvas, 256, 256, 256, 256, (1,1,0,1))
# canvas.render("simple-viewport.png")
plt.show()

