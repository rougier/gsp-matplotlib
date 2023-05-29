# -----------------------------------------------------------------------------
# Graphic Server Protocol (GSP)
# Copyright 2023 Vispy Development Team - BSD 2 Clauses licence
# -----------------------------------------------------------------------------
import numpy as np
from gsp.glm import mat4, tracked_array
from gsp.transform import Transform, Mat4
from gsp.core import Viewport, Buffer, Color
from gsp.visual import Visual


class Pixels(Visual):

    def __init__(self, viewport : Viewport,
                       positions : Transform | Buffer,
                       colors : Transform | Buffer | Color = Color(0,0,0,1)):
        """
        Collection of pixels.

        Parameters:

          viewport:

            Viewport where this visual will be renderdd
        
          positions:
        
            Pixels position (vec3)

          colors:
        
            Pixels colors (vec4)
        """

        Visual.__init__(self, viewport)

        self.set_attribute("positions", positions)
        self.set_variable("colors", colors)
        
        kwargs = {}
        if self.is_uniform("colors"):
            kwargs["facecolors"] = colors
        kwargs["marker"] = ","
            
        # Even with antialias off, marker coverage leaks on
        # neighbouring pixels if the position is not an exact divider
        # of viewport size (in pixels). We could round vertices at
        # time of rendering but it is easier to set a very small size
        # whose coverage is more or less guaranteed to be one pixel.
        size = 0.25*(72/self._viewport._canvas._dpi)**2
        self._scatter = self._viewport._axes.scatter( [],[], size, **kwargs)
        self._scatter.set_antialiaseds(True)
        self._scatter.set_linewidths(0)
        
        canvas = self._viewport._canvas._figure.canvas
        canvas.mpl_connect('resize_event', lambda event: self.render())


    def render(self, transform : Transform = None):
        """
        Render the visual using given transform

        Parameters:

          transform: 

            Model/view/projection transform to use
        """

        # Update transform
        self._transform.set_data(transform)

        # Get positions
        positions = self.get_attribute("positions")
        if self.is_transform("positions"):
            positions = positions.evaluate(self._uniforms,
                                           self._attributes)
        else:
            positions = np.asanyarray(positions)
        positions = positions.reshape(-1,3)
        positions = self._transform(positions)[:,:2]
        self._scatter.set_offsets(positions[:,:2])

        # Set attributes
        if (colors := self.eval_variable("colors")) is not None:
            self._scatter.set_facecolors(colors)

            
