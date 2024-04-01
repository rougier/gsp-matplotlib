# Package: Graphic Server Protocol / Matplotlib
# Authors: Nicolas P .Rougier <nicolas.rougier@inria.fr>
# License: BSD 3 clause

"""
This example shows how to create multiple viewports, each with their
own interactive camera that are kept in sync.
"""

import glm
import camera
import numpy as np
from gsp import core, visual, transform

canvas = core.Canvas(512, 512, 100.0)
viewports = [core.Viewport(canvas, 0.0, 0.0, 0.5, 0.5, (1,0,0,.25)),
             core.Viewport(canvas, 0.0, 0.5, 0.5, 0.5, (0,1,0,.25)),
             core.Viewport(canvas, 0.5, 0.0, 0.5, 0.5, (0,0,1,.25)),
             core.Viewport(canvas, 0.5, 0.5, 0.5, 0.5, (1,1,0,.25))]

colormap = transform.Colormap("magma")
depth    = transform.Depth("positions")
positions = glm.vec3(1_000)
positions.xyz = np.random.uniform(-1, +1, (len(positions),3))
fill_colors = glm.vec4(1_000)
fill_colors = colormap(depth)
black = core.Color(0,0,0,1)
points = visual.Points(positions, 25, fill_colors, black, 0.25)

def render(viewport, model, view, proj):
    global viewports, cameras, points
    index = viewports.index(viewport)
    trackball = cameras[index].trackball
    for cam in cameras:
        cam.model = model
        cam.trackball._rotation = trackball._rotation
        cam.trackball._model = trackball._model
        cam.trackball._count = trackball._count
    for viewport in viewports:
        points.render(viewport, model, view, proj)

cameras = []
for viewport in viewports:
    cam = camera.Camera("perspective", theta=10, phi=10)
    cameras.append(cam)
    points.render(viewport, cam.model, cam.view, cam.proj)
    cam.connect(viewport, "motion",  render)

import matplotlib.pyplot as plt
plt.show()
