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

positions = glm.vec3(250_000)
positions.xyz = np.random.uniform(-1, +1, (len(positions),3))
pixels = visual.Pixels(viewport, positions, core.Color(0,0,0,1))
pixels.render(camera.transform)

camera.connect(viewport._axes, "motion",  pixels.render)
plt.show()
