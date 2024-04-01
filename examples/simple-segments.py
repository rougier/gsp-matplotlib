# Package: Graphic Server Protocol / Matplotlib
# Authors: Nicolas P .Rougier <nicolas.rougier@inria.fr>
# License: BSD 3 clause
""" Segments example """

import glm
import camera
import numpy as np
from gsp import core, visual, transform

canvas = core.Canvas()
viewport = core.Viewport(canvas)
camera = camera.Camera("ortho")

n = 50
P = glm.vec3(2*n).reshape(-1,2,3)
P[:] = (0.0, -0.5, 0.0), (0.0, +0.5, 0.0)
P[:,0,0] = np.linspace(-0.75, +0.75, n)
P[:,1,0] = P[:,0,0] + 0.1
LW = np.linspace(0.1, 5.0, n)
segments = visual.Segments(P, line_widths=LW)
segments.render(viewport, camera.model, camera.view, camera.proj)
camera.connect(viewport, "motion",  segments.render)

import matplotlib.pyplot as plt
plt.show()
