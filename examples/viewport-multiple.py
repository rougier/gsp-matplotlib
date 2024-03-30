# Package: Graphic Server Protocol / Matplotlib
# Authors: Nicolas P .Rougier <nicolas.rougier@inria.fr>
# License: BSD 3 clause
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
