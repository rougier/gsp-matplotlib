# Package: Graphic Server Protocol / Matplotlib
# Authors: Nicolas P .Rougier <nicolas.rougier@inria.fr>
# License: BSD 3 clause
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

from gsp.core import Buffer
from gsp.transform import Transform

class Colormap(Transform):
    def __init__(self,
                 colormap : str = None):
        """
        Colormap transform allows to map a scalar to a color

        Parameters:

          colormap:

            Name of the colormap
        """
        Transform.__init__(self)
        self._colormap = colormap


    def set_colormap(self, colormap : str ):
        """
        Set the colormap

        parameters:

          colormap:

            Name of the colormap
        """

    def copy(self):
        """
        Copy the transform
        """
        transform = Transform.copy(self)
        transform._colormap = self._colormap
        return transform


    def evaluate(self, buffers):
        """
        Evaluate the transform
        """

        if self._next:
            value = self._next.evaluate(buffers)
        else:
            value = self._buffer
        cmap = plt.get_cmap(self._colormap)
        norm = mpl.colors.Normalize(vmin=value.min(), vmax=value.max())
        return cmap(norm(value))
