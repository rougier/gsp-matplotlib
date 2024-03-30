# Package: Graphic Server Protocol / Matplotlib
# Authors: Nicolas P .Rougier <nicolas.rougier@inria.fr>
# License: BSD 3 clause
"""
# Simple marker example

This example show different markers/sizes/angles in the same visual.
"""

import numpy as np
import matplotlib.pyplot as plt
from gsp import core, visual, transform, glm

canvas   = core.Canvas(512, 512, 100.0)
viewport = core.Viewport(canvas, 0, 0, 512, 512)
camera   = glm.Camera("perspective", theta=10, phi=10)
colormap = transform.Colormap("magma")

positions = glm.vec3(1000)
positions.xyz = np.random.uniform(-1, +1, (1000,3))
fill = colormap(transform.ScreenZ())
black = core.Color(0,0,0,1)
types = np.array([core.Marker.star,    ]*500 +
                 [core.Marker.triangle,]*500)
angles = np.random.uniform(0, 360, 1000)

points = visual.Markers(
    viewport, positions, types, 250, angles, fill, black, .5)
points.render( camera.transform )

camera.connect(viewport._axes, "motion",  points.render)
plt.show()
