# -----------------------------------------------------------------------------
# Graphic Server Protocol (GSP)
# Copyright 2023-2024 Cyrille Rossant & Nicolas Rougier - BSD 2 Clauses licence
# -----------------------------------------------------------------------------
"""
This example demonstrates how to specify margins expressed in
pixels when creating a viewport.
"""
import matplotlib.pyplot as plt
from gsp import core, transform

canvas = core.Canvas(512, 512, 100.0)
pixel = transform.Pixel()
viewport = core.Viewport(canvas, x = 10*pixel,
                                 y = 10*pixel,
                                 width = 1.0 - 20*pixel,
                                 height = 1.0 - 20*pixel,
                                 color = (1,1,1,1))
plt.show()
