# Examples

## Quick start

For the impatient, here is a small example that display 10,000 points
whose colors are computed from a colormap linked to the screen depth
of each points. It can be directly saved to an image file or be made
interactive to rotate it with the mouse. 

```python
import gsp
import numpy as np

canvas   = gsp.core.Canvas(512, 512, 100)
viewport = gsp.core.Viewport(canvas, 0, 0, 512, 512)
camera   = gsp.glm.Camera("perspective")

P = gsp.glm.vec3(10_000)
P.xyz = np.random.uniform(-1,+1,(len(P),3))

colormap = gsp.transform.Colormap("magma")
FC = colormap(transform.ScreenZ()) # fill colors
LC = gsp.core.Color(0,0,0,1)       # line colors
S = 25                             # size
LW = 0.25                          # line width

points = gsp.visual.Points(viewport, P, S, FC, LC, LW)
points.render(camera.transform)

canvas.render("output.png")
```

## Simple

* [**simple-canvas.py**](simple-canvas.py) — This example demonstrates
  how to open a canvas and save the result into an image filename.

* [**simple-viewport.py**]() — This example demonstrates how to
  organize viewports on the canvas.

* [**simple-scatter-2D.py**]() — This example renders a
  two-dimensional scatter plot using an orthographic camera.

* [**simple-scatter-3D.py**]() — This example renders a
  three-dimensional scatter plot using a perspective camera and a
  trackball.

* [**simple-selection.py**]() — This example renders a
  three-dimensional scatter plot and color the points under mouse with
  a different color.

## Basic


* [**points.py**]() — This example demonstrates usage of the JIT (just in
  time buffers). It is used with a colormap to vary color according to
  the depth (screen z) of a point (not to be confused with the z
  coordinate).

