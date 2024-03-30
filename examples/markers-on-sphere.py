# Package: Graphic Server Protocol / Matplotlib
# Authors: Nicolas P .Rougier <nicolas.rougier@inria.fr>
# License: BSD 3 clause
""" Simple markers """
import numpy as np
import matplotlib.pyplot as plt
from gsp import core, visual, transform, glm

canvas   = core.Canvas(512, 512, 100.0)
viewport = core.Viewport(canvas, 0, 0, 512, 512)
camera   = glm.Camera("perspective", theta=-20, phi=2.5)
colormap = transform.Colormap("gray_r")
depth    = transform.Depth("positions")

n = 256
P = glm.vec3(n)
T = np.pi * (3 - np.sqrt(5)) * np.arange(n)
Z = np.linspace(1 - 1.0 / n, 1.0 / n - 1, n)
R = np.sqrt(1 - Z*Z)
P.xy = R*np.sin(T), R*np.cos(T)
P.z = Z
points = visual.Markers(P, [core.Marker.star]*n, sizes=256,
                        axis = P,
                        fill_colors = colormap(depth))
points.render(viewport, camera.model, camera.view, camera.proj)
camera.connect(viewport, "motion",  points.render)
plt.savefig("../docs/assets/simple-markers.png")
plt.show()
