# Package: Graphic Server Protocol / Matplotlib
# Authors: Nicolas P .Rougier <nicolas.rougier@inria.fr>
# License: BSD 3 clause
"""
# Simple light example

This example doesn't do much, it just makes a simple plot
"""
from gsp.core import Canvas

canvas = Canvas(512, 512, 100.0)
canvas.render("simple-canvas.png")
