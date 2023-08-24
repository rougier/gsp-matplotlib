# -----------------------------------------------------------------------------
# Graphic Server Protocol (GSP)
# Copyright 2023 Vispy Development Team - BSD 2 Clauses licence
# -----------------------------------------------------------------------------
""" Segments example """

import numpy as np
import matplotlib.pyplot as plt
from gsp import core, visual, transform, glm

canvas = core.Canvas(512, 512, 100.0)
viewport = core.Viewport(canvas, 0, 0, 512, 512)
camera = glm.Camera("ortho")

n = 50
P = glm.vec3(2*n).reshape(-1,2,3)
P[:] = (0.0, -0.5, 0.0), (0.0, +0.5, 0.0)
P[:,0,0] = np.linspace(-0.75, +0.75, n)
P[:,1,0] = P[:,0,0] + 0.1
LW = np.linspace(0.1, 5.0, n)
points = visual.Segments(P, line_widths=LW)
points.render(viewport, camera.model, camera.view, camera.proj)

# plt.savefig("../docs/assets/simple-segments.png")
plt.show()

