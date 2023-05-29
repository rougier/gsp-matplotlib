# -----------------------------------------------------------------------------
# Graphic Server Protocol (GSP)
# Copyright 2023 Vispy Development Team - BSD 2 Clauses licence
# -----------------------------------------------------------------------------
"""
# Zoom integration is point sizes and line widths.

This example demonstrates the dynamic modification of the sizes and the
linewidths of a collection of points such that they visually grow and
shrink with zoom level. 
"""
import numpy as np
import matplotlib.pyplot as plt
from gsp import core, visual, transform, glm

canvas   = core.Canvas(512, 512, 100.0)
viewport = core.Viewport(canvas, 0, 0, 512, 512)
camera   = glm.Camera("perspective", theta=10, phi=10)
colormap = transform.Colormap("magma")
depth    = transform.ScreenZ()

n = 5_000
positions = glm.vec3(n)
positions.xyz = np.random.uniform(-1, +1, (n,3))

fill_colors = colormap(depth)
black = core.Color(0,0,0,1)

_sizes = np.random.uniform(25, 50, n)
sizes = glm.scalar(n)
sizes[...] = _sizes

_linewidths = 0.25
linewidths = glm.scalar(1)
linewidths[...] = _linewidths

def update(transform):
    sizes[...] =  1/(camera.zoom**2) * _sizes
    linewidths[...] = 1/(camera.zoom) * _linewidths
    points.render(transform)

points = visual.Points(viewport, positions, sizes,
                       fill_colors, black, linewidths)
points.render(camera.transform)


camera.connect(viewport._axes, "motion",  points.render)
camera.connect(viewport._axes, "scroll",  update)
plt.show()

