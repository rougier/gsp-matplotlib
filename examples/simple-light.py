# -----------------------------------------------------------------------------
# Graphic Server Protocol (GSP)
# Copyright 2023 Vispy Development Team - BSD 2 Clauses licence
# -----------------------------------------------------------------------------
"""
# Simple light example

This example doesn't do much, it just makes a simple plot
"""

import numpy as np
from gsp import glm, core, visual, transform

canvas   = core.Canvas(512, 512, 100.0)
viewport = core.Viewport(canvas, 0, 0, 512, 512)
camera   = glm.Camera("ortho")

V, I = glm.sphere(0.25, 64, 64)
F = V[I]
        
for x, d in zip(np.linspace(-0.75, 0.75, 4), [0.00, 0.25, 0.5, 0.75]):
    for y, shininess in zip(np.linspace(0.75, -0.75, 4), [0, 8, 16, 32]):
        ambient  = 1.0, 0.0, 0.0, 1-d
        diffuse  = 1.0, 0.1, 0.1, d
        specular = 1.0, 1.0, 1.0, shininess
        light = transform.Light((1.0,0.5,1.5), ambient, diffuse, specular)
        mesh = visual.Mesh(V, I, None, light(F), core.Color(0,0,0,0), 0)
        mesh.render(viewport, camera.transform @ glm.translate(x,y,0))

import matplotlib.pyplot as plt
plt.show()

