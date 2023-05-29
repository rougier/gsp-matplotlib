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
from gsp import glm, core, visual, transform

canvas   = core.Canvas(512, 512, 100.0)
viewport = core.Viewport(canvas, 0, 0, 512, 512)
camera   = glm.Camera("perspective", theta=-20, phi=2.5)
colormap = transform.Colormap("magma")
depth    = transform.Depth()

V,F = glm.mesh("data/bunny-4096.obj")
EC = core.Color(0.00, 0.00, 0.00, 1.00)
FC = colormap(depth)

mesh = visual.Mesh(viewport, V, F, FC, EC, 0)
mesh.render(camera.transform)

camera.connect(viewport._axes, "motion",  mesh.render)
plt.show()

