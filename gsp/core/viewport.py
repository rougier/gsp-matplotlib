# -----------------------------------------------------------------------------
# Graphic Server Protocol (GSP)
# Copyright 2023 Vispy developmet team - BSD 2 Clauses licence
# -----------------------------------------------------------------------------
import numpy as np
from . canvas import Canvas
from . types import Color

class Viewport:
        
    def __init__(self, canvas : Canvas,
                       x :      int = 0,
                       y :      int = 0,
                       width :  int = None,
                       height : int = None,
                       color :  Color = Color(0,0,0,0)):
        """
        A viewport is a rectangular two-dimensional surface of a
        canvas, located at (x, y) coordinates (bottom left corner)
        with size equal to width×height pixels.
        
        !!! Note

            Future implementation will allows viewports to have an
            arbitrary rotation.

        Parameters:

          canvas:
        
            Canvas where to create the viewport

          x:
        
            X coordinate of the viewport bottom left corner
        
          y:
        
            Y coordinate of the viewport bottom left corner
        
          width:

            Width of the viewport in pixels.
        
          height:

            Height of the viewport in pixels.

          color:

            Background color of the viewport
        """

        self._canvas = canvas
        width = width or canvas._width
        height = height or canvas._height
        self._color = color
        self._extent = x, y, width, height
        self._axes = canvas._figure.add_axes([x / canvas._width,
                                              y / canvas._height,
                                              width / canvas._width,   
                                              height / canvas._height])
        self._axes.set_aspect(width/height)
        self._axes.patch.set_color(self._color)
        # self._axes.patch.set_alpha(0)
        self._axes.autoscale(False)
        self._axes.set_xlim(-1, 1)
        self._axes.set_ylim(-1, 1)
        self._axes.get_xaxis().set_visible(False)
        self._axes.get_yaxis().set_visible(False)
        for position in ["top", "bottom", "left", "right"]:
            self._axes.spines[position].set_visible(False)


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

