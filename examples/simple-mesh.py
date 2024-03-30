# Package: Graphic Server Protocol / Matplotlib
# Authors: Nicolas P .Rougier <nicolas.rougier@inria.fr>
# License: BSD 3 clause
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

V,Vi = glm.mesh("data/bunny-4096.obj")
EC = core.Color(0.00, 0.00, 0.00, 1.00)
FC = core.Color(1.00, 1.00, 1.00, 0.85)
mesh = visual.Mesh(V, Vi, None, FC, EC, 0.25)
mesh.render(viewport, camera.model, camera.view, camera.proj)

camera.connect(viewport, "motion",  mesh.render)
# plt.savefig("../docs/assets/simple-mesh.png")
plt.show()
