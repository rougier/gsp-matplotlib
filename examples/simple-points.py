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
camera   = glm.Camera("ortho")

n = 600
positions = np.zeros((n,3))
R = np.linspace(0.05, 0.95, n)
T = np.linspace(0, 10.125*2*np.pi, n)
positions[:,0], positions[:,1] = R*np.cos(T), R*np.sin(T)
sizes = np.linspace(0.05, 12.0, n)**2
black, white = core.Color(0,0,0,1), core.Color(1,1,1,1)

points = visual.Points(viewport, positions, sizes, black, black, 0)
points.render( camera.transform )
plt.show()

