# -----------------------------------------------------------------------------
# Graphic Server Protocol (GSP)
# Copyright 2023 Vispy Development Team - BSD 2 Clauses licence
# -----------------------------------------------------------------------------
"""
"""

import numpy as np
import matplotlib.pyplot as plt
from gsp import core, visual, transform, glm

canvas   = core.Canvas(512, 512, 100.0)
viewport = core.Viewport(canvas, 0, 0, 512, 512)
camera   = glm.Camera("ortho")

n = 200
V = np.zeros(n, [ ("position", np.float32, 3),
                  ("size",     np.float32),
                  ("angle",    np.float32),
                  ("type",     np.float32),
                  ("color",    np.float32, 4) ])
R = np.linspace(0.25, 0.95, n)
T = np.linspace(0, 10.125*2*np.pi, n)
V["position"][:,0] = R*np.cos(T)
V["position"][:,1] = R*np.sin(T)
V["size"] = np.linspace(10, 20, n)**2
V["angle"] = 180*T/np.pi - 90
V["type"] = [core.Marker.heart, core.Marker.club,
             core.Marker.diamond, core.Marker.spade]*(n//4)
V["color"] = [(1,0,0,1), (0,0,0,1), (1,0,0,1), (0,0,0,1)]*(n//4)
black, white = core.Color(0,0,0,1), core.Color(0,0,0,1)

points = visual.Markers(viewport, V["position"], V["type"], V["size"],
                                  V["angle"], V["color"], black, 0)
points.render( camera.transform )
plt.show()


