
For the impatient, here is a small example that display 10,000 points
whose colors are computed from a colormap linked to the screen depth
of each points. It can be directly saved to an image file or be made
interactive to rotate it with the mouse. 

```python

import gsp
import numpy as np

canvas = gsp.core.Canvas(512, 512, 100)
viewport = gsp.core.Viewport(canvas, 0, 0, 512, 512)
camera = gsp.glm.Camera("perspective")

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
