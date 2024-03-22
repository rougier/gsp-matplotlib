# -----------------------------------------------------------------------------
# Graphic Server Protocol (GSP)
# Copyright 2023 Vispy Development Team - BSD 2 Clauses licence
# -----------------------------------------------------------------------------
import numpy as np
from gsp import glm
from gsp.visual import Visual
from gsp.core import Viewport, Buffer, Color


class Pixels(Visual):
    """
    Pixels are the smallest entities that can be rendered on screen (pixel or fragment) or on paper (dot). They can be colored but have no dimension and correspond to the true mathematical notion of a point.

    !!! Notes "Notes on matplotlib implementation"

        Even with antialias off, marker coverage leaks on neighbouring pixels if the position is not an exact divider of viewport size (in pixels). Vertices coordinates could be rounded at time of rendering but it is easier to set a very small size whose coverage is more or less guaranteed to be one pixel. However, this size seems to be wrong on Windows, depending on the screen size.
    """

    def __init__(self, positions,
                       colors  = Color(0,0,0,1)):
        """
        Create a visual of n pixels at given *positions* with
        given *colors*.

        Parameters
        ----------
        positions : Transform | Buffer
            Pixels position (vec3)
        colors : Transform | Buffer | Color
            Pixels colors (vec4)
        """

        Visual.__init__(self)
        self.set_variable("positions", positions)
        self.set_variable("colors", colors)

    def render(self, viewport, model=None, view=None, proj=None):
        """
        Render the visual on *viewport* using the given *model*,
        *view*, *proj* matrices

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
            size = 0.25*(72/viewport._canvas._dpi)**2
            collection = viewport._axes.scatter( [],[], size)
            collection.set_antialiaseds(True)
            collection.set_linewidths(0)
            self._viewports[viewport] = collection
            viewport._axes.add_collection(collection, autolim=False)

            # This is necessary for measure transforms that need to be
            # kept up to date with canvas size
            canvas = viewport._canvas._figure.canvas
            canvas.mpl_connect('resize_event',
                               lambda event: self.render(viewport))

        collection = self._viewports[viewport]
        positions = self.eval_variable("positions")
        positions = positions.reshape(-1,3)
        positions = glm.to_vec3(glm.to_vec4(positions) @ transform.T)
        collection.set_offsets(positions[:,:2])
        colors = self.eval_variable("colors")
        if colors is not None:
            collection.set_facecolors(colors)
