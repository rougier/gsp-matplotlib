# Package: Graphic Server Protocol / Matplotlib
# Authors: Nicolas P .Rougier <nicolas.rougier@inria.fr>
# License: BSD 3 clause
""" Points example """

import glm
import camera
import numpy as np
from gsp import core, visual, transform

canvas   = core.Canvas(512, 512, 100.0)
viewport = core.Viewport(canvas, 0, 0, 512, 512)
camera   = camera.Camera("ortho")

n = 600
P = glm.vec3(n)
R = np.linspace(0.05, 0.95, n)
T = np.linspace(0, 10.125*2*np.pi, n)
P.xy = R*np.cos(T), R*np.sin(T)
sizes = np.linspace(0.05, 12.0,n)**2
black, white = core.Color(0,0,0,1), core.Color(1,1,1,1)
points = visual.Points(P, sizes, black, black, 0)
points.render(viewport, camera.model, camera.view, camera.proj)

import matplotlib.pyplot as plt
plt.show()
