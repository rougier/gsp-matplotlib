# Package: Graphic Server Protocol / Matplotlib
# Authors: Nicolas P .Rougier <nicolas.rougier@inria.fr>
# License: BSD 3 clause
"""
This example shows how to use physical dimensions. The inner
square has a fixed size, while the outer square has a proprotional
size. This becomes obvious when canvas is resized.
"""

import glm
import camera
import numpy as np
from gsp import core, visual, transform

canvas = core.Canvas()
viewport = core.Viewport(canvas)
camera = camera.Camera(mode="ortho")
pixel = transform.Pixel()

P = glm.vec3((4,2))
P[0] =  (-0.75, -0.75,0), (-0.75,  0.75,0)
P[1] = (-0.75,  0.75,0), ( 0.75,  0.75,0)
P[2] = ( 0.75,  0.75,0), ( 0.75, -0.75,0)
P[3] = ( 0.75, -0.75,0), (-0.75, -0.75,0)
S = visual.Segments(P, line_colors=(0,0,0,1))
S.render(viewport, camera.model, camera.view, camera.proj)

P = glm.vec3((4,2))
P[0] = (-128, -128,0), (-128,  128,0)
P[1] = (-128,  128,0), ( 128,  128,0)
P[2] = ( 128,  128,0), ( 128, -128,0)
P[3] = ( 128, -128,0), (-128, -128,0)
S = visual.Segments(P*pixel, line_colors=(0,0,0,1))
S.render(viewport, camera.model, camera.view, camera.proj)

import matplotlib.pyplot as plt
plt.show()
