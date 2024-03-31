# Package: Graphic Server Protocol / Matplotlib
# Authors: Nicolas P .Rougier <nicolas.rougier@inria.fr>
# License: BSD 3 clause

"""
This example demonstrates how to specify margins expressed in
pixels (or inches, centimeters, etc) when creating a viewport.
"""

from gsp import core, transform

canvas = core.Canvas(512, 512, 100.0)
pixel = transform.Pixel()
viewport = core.Viewport(canvas, x = 10*pixel,
                                 y = 10*pixel,
                                 width = 1.0 - 20*pixel,
                                 height = 1.0 - 20*pixel,
                                 color = (1,1,1,1))

import matplotlib.pyplot as plt
plt.show()
