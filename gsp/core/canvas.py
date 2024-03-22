# -----------------------------------------------------------------------------
# Graphic Server Protocol (GSP)
# Copyright 2023 Vispy Development Team - BSD 2 Clauses licence
# -----------------------------------------------------------------------------
import io
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

class Canvas:
    """
    A Canvas is a two-dimensional drawing area of size
    width × height pixels using the specified dpi (dots per
    inch).

    !!! Note

        - A canvas uses a standard color space with at least 8 bits per channel.
        - Blending mode is alpha blending
        - The `(0,0)` coordinates corresponds to the bottom left corner.
        - A typographical point is 1/72 inch.
    """
    
    def __init__(self, width = 512, height = 512, dpi = 100.0):
        """
        Parameters
        ----------
        width : int
            Width of the drawing area in pixels.
        height : int
            Height of the drawing area in pixels.
        dpi : float
            Dots per inch
        """
        
        self._width = width
        self._height = height
        self._dpi = dpi
        self._figure = plt.figure(frameon=False, dpi=self._dpi)
        self._figure.patch.set_alpha(0.0)
        self._figure.set_size_inches(self._width / self._dpi,
                                    self._height /self._dpi)

        canvas = self._figure.canvas
        canvas.mpl_connect('resize_event', lambda event: self._figure.canvas.draw())
        
        
    @property
    def size(self):
        # figure.dpi cand canvas.dpi might be different because system
        # such as OSX will double the dpi (retina display)
        dpi = self._dpi
        return figure.get_size_inches() * dpi

        
    def render(self, target = None):
        """
        Render the canvas to the specified target. If no target is
        specified, return a raw image as bytes.

        Parameters
        ----------

        target : str
            Filename of the target
        """

        if target is None:
            self._figure.canvas.draw()
            with io.BytesIO() as output:
                self._figure.savefig(output, format="raw")
                output.seek(0)
                data = np.frombuffer(output.getvalue(), dtype=np.uint8)
            return data.reshape(self._height, self._width, -1)
        else:
            self._figure.savefig(target, dpi=self._dpi)
