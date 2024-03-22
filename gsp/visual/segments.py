# -----------------------------------------------------------------------------
# Graphic Server Protocol (GSP)
# Copyright 2023 Vispy Development Team - BSD 2 Clauses licence
# -----------------------------------------------------------------------------
import numpy as np
from gsp import glm
from gsp.visual import Visual
from matplotlib.collections import LineCollection
from gsp.core import Viewport, Buffer, Color, Measure, LineCap


class Segments(Visual):
    """
    !!! Note "Quick documentation"

        === "Definition"

            ![](../../assets/simple-segments.png){ width="33%" align=right }

            Segments are line segments between two vertices. They can
            be colored and styled (dash pattern). They possess a
            thickness but always face the viewer such that their
            apparent thickness is constant. Their end points (caps)
            can be styled following the [SVG
            specification](https://www.w3.org/TR/SVG2/painting.html)
            (butt, round or cap).


        === "Code example"

            ```python
            import numpy as np
            import matplotlib.pyplot as plt
            from gsp import core, visual, transform, glm

            canvas = core.Canvas(512, 512, 100.0)
            viewport = core.Viewport(canvas, 0, 0, 512, 512)
            camera = glm.Camera("ortho")

            n = 50
            P = glm.vec3(2*n).reshape(-1,2,3)
            P[:] = (0.0, -0.5, 0.0), (0.0, +0.5, 0.0)
            P[:,0,0] = np.linspace(-0.75, +0.75, n)
            P[:,1,0] = P[:,0,0] + 0.1
            LW = np.linspace(0.1, 5.0, n)

            points = visual.Segments(P, line_widths=LW)
            points.render(viewport, camera.model, camera.view, camera.proj)
            plt.show()
            ```
    """

    def __init__(self, positions,
                       line_caps = LineCap.round,
                       line_colors = Color(0,0,0,1),
                       line_widths = 1):
        """
        Create a visual of n segments at given *positions* with
        given *line_colors*, *line_widths* and *line_caps*.

        Parameters
        ----------
        positions : Transform | Buffer
            Points position (vec3)
        line_caps : Transform | Buffer
            Line caps (vec2)
        line_colors : Transform | Buffer | Color
            Points line colors (vec4)
        line_widths : Transform | Buffer | Measure
            Points line colors (vec4)
        """

        Visual.__init__(self)
        self.set_variable("positions", positions)
        self.set_variable("line_caps", line_caps)
        self.set_variable("line_colors", line_colors)
        self.set_variable("line_widths", line_widths)


    def render(self, viewport=None, model=None, view=None, proj=None):
        """
        Render the visual on *viewport* using the given *model*,
        *view*, *proj* matrices.

        Parameters
        ----------
        viewport : Viewport
            Viewport where to render the visual
        model : mat4
            Model matrix to use for rendering
        view : mat4
            View matrix to use for rendering
        proj : mat4
            Projection matrix to use for rendering
        """

        # We store the model/view/proj matrices for the resize_event below
        if model is not None:
            self._model = model
        model = self._model

        if view is not None:
            self._view = view
        view = self._view

        if proj is not None:
            self._proj = proj
        proj = self._proj

        transform = proj @ view @ model
        self.set_variable("viewport", viewport)

        # Create the collection if necessary
        if viewport not in self._viewports:
            collection = LineCollection([], clip_on=True, snap=False)
            self._viewports[viewport] = collection
            viewport._axes.add_collection(collection, autolim=False)

            # This is necessary for measure transforms that need to be
            # kept up to date with canvas size
            canvas = viewport._canvas._figure.canvas
            canvas.mpl_connect('resize_event', lambda event: self.render(viewport))

        collection = self._viewports[viewport]
        positions = self.eval_variable("positions")
        positions = positions.reshape(-1,3)
        positions = glm.to_vec3(glm.to_vec4(positions) @ transform.T)
        positions = positions.reshape(-1,2,3)

        depth = -positions[:,:,2].mean(axis=1)
        sort_indices = np.argsort(depth)
        positions = positions[sort_indices]
        collection.set_segments(positions[...,:2])
        self.set_variable("screen", {"positions": positions,
                                     "segments": positions.mean(axis=1)})
        self.set_variable("depth",  {"positions": positions[:2],
                                     "segments" : depth})

        line_colors = self.eval_variable("line_colors")
        if isinstance(line_colors, np.ndarray) and (len(line_colors) == len(positions)):
            collection.set_edgecolors(line_colors[sort_indices])
        else:
            collection.set_edgecolors(line_colors)

        line_widths = self.eval_variable("line_widths")
        if isinstance(line_widths, np.ndarray) and (len(line_widths) == len(positions)):
            collection.set_linewidths(line_widths[sort_indices])
        else:
            collection.set_linewidths(line_widths)
