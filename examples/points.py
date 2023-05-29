# -----------------------------------------------------------------------------
# Graphic Server Protocol (GSP)
# Copyright 2023 Vispy Development Team - BSD 2 Clauses licence
# -----------------------------------------------------------------------------
"""
# Simple light example

This example doesn't do much, it just makes a simple plot
"""

import numpy as np
import matplotlib.pyplot as plt
from gsp import core, visual, transform, glm

canvas   = core.Canvas(512, 512, 100.0)
viewport = core.Viewport(canvas, 0, 0, 512, 512)
camera   = glm.Camera("perspective", theta=10, phi=10)
colormap = transform.Colormap("magma")
depth    = transform.ScreenZ()

positions = glm.vec3(10_000)
positions.xyz = np.random.uniform(-1, +1, (len(positions),3))

fill_colors = glm.vec4(10_000)
fill_colors = colormap(depth)
black = core.Color(0,0,0,1)

points = visual.Points(viewport, positions, 25, fill_colors, black, 0.25)
points.render( camera.transform )

# canvas.render("../docs/assets/points.png")
camera.connect(viewport._axes, "motion",  points.render)
plt.show()

