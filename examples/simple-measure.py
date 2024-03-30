# -----------------------------------------------------------------------------
# Graphic Server Protocol (GSP)
# Copyright 2023 Vispy Development Team - BSD 2 Clauses licence
# -----------------------------------------------------------------------------
"""
# Fixed placement

This example demonstrates how to position objects at a fixed location that can be expressed in pixels, inches or centimeters.
"""
import numpy as np
from gsp import core, visual, transform, glm

canvas = core.Canvas(512, 512, 100.0)
viewport = core.Viewport(canvas)
camera = glm.Camera(mode="ortho")
pixel = transform.Pixel()
inch = transform.Inch()
cm = transform.Centimeter()

O = np.array([-1.0, -1.0, 0])

P1 = O + [0.25, 0.25, 0]
p1 = visual.Points(P1, fill_colors=(0,0,0,1))
p1.render(viewport, camera.model, camera.view, camera.proj)

P2 = O + (256,256,0)*pixel
p2 = visual.Points(P2, fill_colors=(1,0,0,1))
p2.render(viewport, camera.model, camera.view, camera.proj)

P3 = O + (1,1,0)*inch
p3 = visual.Points(P3, fill_colors=(0,1,0,1))
p3.render(viewport, camera.model, camera.view, camera.proj)

P4 = O + (1,1,0)*cm
p4 = visual.Points(P4, fill_colors=(0,0,1,1))
p4.render(viewport, camera.model, camera.view, camera.proj)

import matplotlib.pyplot as plt
plt.show()
