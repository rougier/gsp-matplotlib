# Package: Graphic Server Protocol / Matplotlib
# Authors: Nicolas P .Rougier <nicolas.rougier@inria.fr>
# License: BSD 3 clause
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
depth    = transform.Depth("positions")

n = 5_000
positions = glm.vec3(n)
positions.xyz = np.random.uniform(-1, +1, (n,3))

fill_colors = colormap(depth)
black = core.Color(0,0,0,1)

_sizes = np.random.uniform(25, 50, n)
sizes = np.ones(n)
sizes[...] = _sizes

_linewidths = 0.25
linewidths = np.ones(1)
linewidths[...] = _linewidths

def update(viewport, model, view, proj):
    sizes[...] =  1/(camera.zoom**2) * _sizes
    linewidths[...] = 1/(camera.zoom) * _linewidths
    points.render(viewport, model, view, proj)

points = visual.Points(positions, sizes, fill_colors, black, linewidths)
points.render(viewport, camera.model, camera.view, camera.proj)
camera.connect(viewport, "motion",  points.render)
camera.connect(viewport, "scroll",  update)
plt.show()
