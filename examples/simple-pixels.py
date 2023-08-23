# -----------------------------------------------------------------------------
# Graphic Server Protocol (GSP)
# Copyright 2023 Vispy Development Team - BSD 2 Clauses licence
# -----------------------------------------------------------------------------
"""
This example show the Pixels visual where pixels are spread
randomly inside a cube that can be rotated using the mouse.
"""
import numpy as np
import matplotlib.pyplot as plt
from gsp import glm, core, visual, transform

canvas   = core.Canvas(512, 512, 100.0)
viewport = core.Viewport(canvas, 0, 0, 512, 512)
camera   = glm.Camera("perspective", theta=50, phi=50)

P = glm.vec3(250_000)
P.xyz = np.random.uniform(-1, +1, (len(P),3))
pixels = visual.Pixels(P)
pixels.render(viewport, camera.model, camera.view, camera.proj)
camera.connect(viewport, "motion",  pixels.render)
# plt.savefig("../docs/assets/simple-pixels.png")
plt.show()
