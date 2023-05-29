# -----------------------------------------------------------------------------
# Graphic Server Protocol (GSP) — matplotlib backend
# Copyright 2023 Vispy Development Team - BSD 2 Clauses licence
# -----------------------------------------------------------------------------
import numpy as np
from gsp.core import Buffer
from gsp.transform import Transform

class Measure(Transform):
    """
    A Measure transform allows to convert a measure expressed in
    some units (Pixel, Point, Inch, etc.) to normalized device
    coordinates ([-1,+1] x [-1,+1]). This conversion is always
    relative to a given [Viewport][gsp.core.Viewport] whose width and
    height dictates the conversion.

    !!! Note

        The normalization of a measure (conversion to NDC) migth be
        different on the x or y axis depending on the size of the
        related viewport. This means, for example, that the expression
        `10*pixel` is translated differently along `x` (1st compoeent)
        and `y` axis (second component).

        The `z` coordinate is not changed during conversion since
        measure are targeting 2D coordinates.

    Examples:

    ``` python
    canvas = core.Canvas(512, 512, 100.0)
    viewport = core.Viewport(canvas, color=(1,1,0,1))

    # 10 pixels from bottom left corner
    pixel = transform.Pixel()
    P = [-1,-1,0] + 10*pixel

    # 10 points from left, 20 points from bottom
    point = transform.Point()
    P = [-1,-1,0] + (10,20,0)*point
    ```
    """

    # See https://numpy.org/doc/stable/user/c-info.beyond-basics.html
    __array_priority__ = 2

    def evaluate(self, uniforms, attributes):
        """
        Evaluate the transform
        """

        if "viewport" not in uniforms.keys():
            raise ValueError("Viewport has not been specified")
        if self._next:
            buffer = self._next.evaluate(uniforms, attributes)
        elif self._buffer is not None:
            buffer = self._buffer
        else:
            raise ValueError("Transform is not bound")

        buffer = np.asanyarray(buffer)
        width, height = uniforms["viewport"].size
        dpi = uniforms["viewport"]._canvas._dpi
        
        # "2" because normalized device coordinates goes from -1 to +1
        scale = np.array([2/width, 2/height, 0])
        
        if len(buffer.shape) == 0 or buffer.shape[-1] == 1: 
            scale = scale[0]
        elif buffer.shape[-1] == 2: 
            scale = scale[:2]
        return scale * buffer
    
    
    def __mul__(self, other):
        if isinstance(other, (int,tuple)):
            return self(other)
        return Transform.__mul__(self, other)

    def __rmul__(self, other):
        return self.__mul__(other)

    
class Pixel(Measure):
    """
    Conversion of a measure to pixel.
    """
    
    def evaluate(self, uniforms, attributes):
        """Evaluate the transform"""

        measure = Measure.evaluate(self, uniforms, attributes)
        return measure


class Inch(Measure):
    """
    Conversion of a measure to inch.
    """
    
    def evaluate(self, uniforms, attributes):
        """Evaluate the transform"""

        measure = Measure.evaluate(self, uniforms, attributes)
        dpi = uniforms["viewport"]._canvas._dpi
        return dpi * measure

class Point(Measure):
    """
    Conversion of a measure to point
    """
    
    def evaluate(self, uniforms, attributes):
        """Evaluate the transform"""

        measure = Measure.evaluate(self, uniforms, attributes)
        dpi = uniforms["viewport"]._canvas._dpi
        return dpi/72 * measure

class Centimeter(Measure):
    """
    Conversion of a measure to centimeter
    """
    
    def evaluate(self, uniforms, attributes):
        """Evaluate the transform"""

        measure = Measure.evaluate(self, uniforms, attributes)
        dpi = uniforms["viewport"]._canvas._dpi
        return dpi/2.54 * measure

class Millimeter(Measure):
    """
    Conversion of a measure to millimeter
    """
    
    def evaluate(selfk, uniforms, attributes):
        """Evaluate the transform"""

        measure = Measure.evaluate(self, uniforms, attributes)
        dpi = uniforms["viewport"]._canvas._dpi
        return 0.1*dpi/2.54 * measure

class Meter(Measure):
    """
    Conversion of a measure to meter
    """
    
    def evaluate(self, uniforms, attributes):
        """Evaluate the transform"""

        measure = Measure.evaluate(self, uniforms, attributes)
        dpi = uniforms["viewport"]._canvas._dpi
        return 10e2*dpi/2.54 * measure

class Kilometer(Measure):
    """
    Conversion of a measure to kilometer
    """
    
    def evaluate(self, uniforms, attributes):
        """Evaluate the transform"""

        measure = Measure.evaluate(self, uniforms, attributes)
        dpi = uniforms["viewport"]._canvas._dpi
        return 1e5*dpi/2.54 * measure
