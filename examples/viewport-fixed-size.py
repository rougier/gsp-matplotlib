# -----------------------------------------------------------------------------
# Graphic Server Protocol (GSP)
# Copyright 2023-2024 Cyrille Rossant & Nicolas Rougier - BSD 2 Clauses licence
# -----------------------------------------------------------------------------
"""
This example demonstrates how to specify margins expressed in
pixels when creating a viewport. When Canvas is resized, these margins
are not enforced because the aspect of the original viewport prevails.
"""
from gsp import core, transform

canvas = core.Canvas(512, 512, 100.0)
pixel = transform.Pixel()
viewport = core.Viewport(canvas, x = 0.5-128*pixel,
                                 y = 0.5-128*pixel,
                                 width = 256*pixel,
                                 height = 256*pixel,
                                 color = (1,1,1,1))

import matplotlib.pyplot as plt
plt.show()
