# Package: Graphic Server Protocol / Matplotlib
# Authors: Nicolas P .Rougier <nicolas.rougier@inria.fr>
# License: BSD 3 clause

"""
This example shows how to create a canvas and save it to a file.
"""

from gsp import core

canvas = core.Canvas(512, 512, 100.0)
canvas.render("./output/canvas-simple.png")
