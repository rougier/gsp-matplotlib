# Package: Graphic Server Protocol / Matplotlib
# Authors: Nicolas P .Rougier <nicolas.rougier@inria.fr>
# License: BSD 3 clause
from __future__ import annotations
import numpy as np
from . canvas import Canvas
from . types import Color

class Viewport:

    """
    A viewport is a rectangular two-dimensional surface of a
    canvas, located at (x, y) coordinates (bottom left corner)
    with size equal to width × height pixels.

    !!! Notes

        Future implementation will allows viewports to have an
        arbitrary rotation.
    """

    def __init__(self, canvas ,
                       x = 0,
                       y = 0,
                       width = 1.0,
                       height = 1.0,
                       color = (1,1,1,1)):
        """
        A viewport is a rectangular two-dimensional surface of a
        canvas, located at (x, y) coordinates (bottom left corner)
        with size equal to width × height pixels.

        Parameters
        ----------

        canvas: Canvas
            Canvas where to create the viewport
        x: int
            X coordinate of the viewport bottom left corner
        y: int
            Y coordinate of the viewport bottom left corner
        width: int
            Width of the viewport in pixels.
        height: int
            Height of the viewport in pixels.
        color: Color
            Background color of the viewport
        """

        self._canvas = canvas
        width = width or canvas._width
        height = height or canvas._height
        self._color = color
        self._extent = x, y, width, height
        self._axes = canvas._figure.add_axes([0,0,1,1])
        self._axes.zoom = 1.0
        self._update()

        self._axes.patch.set_color(self._color)
        # self._axes.patch.set_alpha(0)
        self._axes.autoscale(False)

        # self._axes.set_xlim(-1, 1)
        # self._axes.set_ylim(-1, 1)

        self._axes.get_xaxis().set_visible(False)
        self._axes.get_yaxis().set_visible(False)
        for position in ["top", "bottom", "left", "right"]:
            self._axes.spines[position].set_visible(False)

        # Listen to resize event to adjust position and size
        canvas = self._canvas._figure.canvas
        canvas.mpl_connect('resize_event', lambda event: self._update())


    def _update(self):
        """
        Update viewport position and size
        """

        from .. import transform

        x, y, width, height = self._extent
        canvas = self._canvas
        size = canvas.size

        # Measure transorm cannot know if we evaluate along x or y
        # axis and this is a problem when value such a "1.0" is used
        # in a measure expression. Does 1.0 referes to widht or
        # height? To force evaluation on a given axis we feed it
        # with a uniform size along x or y, depending on context.
        #
        # Another solution would be to have explicit constants such
        # as transform.canvas.width(), transform.viewport.width(), etc.
        if isinstance(x, transform.Transform):
            x = x.evaluate(variables = {"canvas": canvas,
                                        "size" : (size[0], size[0])})
        elif isinstance(x, int):
            x = x / size[0]
        else:
            pass

        if isinstance(y, transform.Transform):
            y = y.evaluate(variables = { "canvas": canvas,
                                         "size" : (size[1], size[1])})
        elif isinstance(y, int):
            y = y / size[1]
        else:
            pass

        if isinstance(width, transform.Transform):
            width = width.evaluate(variables = { "canvas": canvas,
                                                 "size" : (size[0], size[0])})
        elif isinstance(width, int):
            width = width / size[0]
        else:
            pass

        if isinstance(height, transform.Transform):
            height = height.evaluate(variables = { "canvas": canvas,
                                                   "size" : (size[1], size[1])})
        elif isinstance(height, int):
            height = height / size[1]
        else:
            pass

        # Set position and size
        self._axes.set_position([x, y, width, height])

        # Enforce aspect
        # self._axes.set_aspect(width/height)

        width, height = self.size
        zoom = self._axes.zoom
        if width > height:
            xlim = zoom*width/height
            ylim = zoom
        else:
            xlim = zoom
            ylim = zoom*height/width
        self._axes.set_xlim(-xlim, xlim)
        self._axes.set_ylim(-ylim, ylim)
#        self._axes.set_xlim(-zoom, zoom)
#        self._axes.set_ylim(-zoom, zoom)
        return x, y, width, height

    @property
    def xlim(self):
        return self._axes.get_xlim()

    @property
    def ylim(self):
        return self._axes.get_ylim()

    @property
    def size(self):
        """ Get viewport current size (pixels) """

        figure = self._canvas._figure
        dpi = self._canvas._dpi
        axes = self._axes
        transform = figure.dpi_scale_trans.inverted()
        bbox = axes.get_window_extent().transformed(transform)
        width = bbox.width * dpi
        height = bbox.height * dpi
        return width, height
