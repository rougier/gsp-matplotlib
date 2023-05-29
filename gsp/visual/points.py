# -----------------------------------------------------------------------------
# Graphic Server Protocol (GSP)
# Copyright 2023 Vispy Development Team - BSD 2 Clauses licence
# -----------------------------------------------------------------------------
import numpy as np
from gsp.visual import Visual
from gsp.glm import mat4, tracked_array
from gsp.transform import Transform, Mat4
from gsp.core import Viewport, Buffer, Color, Measure


class Points(Visual):
    def __init__(self, viewport :    Viewport,
                       positions :   Transform | Buffer,
                       sizes :       Transform | Buffer | Measure = 25.0,
                       fill_colors : Transform | Buffer | Color   = Color(0,0,0,1),
                       line_colors : Transform | Buffer | Color   = Color(0,0,0,1),
                       line_widths : Transform | Buffer | Measure = 0):
        """
        Collection of points with size and colors.

        Parameters:

          viewport:

            Viewport where this visual will be rendered
        
          positions:
        
            Points position (vec3)

          sizes:
        
            Points size (scalar)

          fill_colors:
        
            Points fill color (vec4)

          line_colors:
        
            Points line color (vec4)

          line_widths:
        
            Points line widths (scalar)
        """

        Visual.__init__(self, viewport)

        # Positions cannot be uniform
        self.set_attribute("positions", positions)

        # Everythng else can be uniform or attribute
        self.set_variable("sizes", sizes)
        self.set_variable("fill_colors", fill_colors)
        self.set_variable("line_colors", line_colors)
        self.set_variable("line_widths", line_widths)
        
        kwargs = {}
        if self.is_uniform("size"):
            kwargs["s"] = sizes
        if self.is_uniform("line_widths"):
            kwargs["linewidth"] = line_widths
        if self.is_uniform("fill_colors"):
            kwargs["facecolors"] = fill_colors
        if self.is_uniform("line_colors"):
            kwargs["edgecolors"] = line_colors
            
        self._scatter = self._viewport._axes.scatter( [],[], **kwargs)
        self._scatter.set_visible(True)
        self._scatter.set_antialiaseds(True)
        

    def set_positions(self, positions):
        """
        Set positions
        
        Parameters:
                
          positions:
        
            Points position (vec3)
        """
        self.set_attribute("positions", positions)
                
    
    def set_sizes(self, sizes):
        """
        Set sizes
        
        Parameters:

          sizes:
        
            Points size (scalar)
        """
        self.set_variable("sizes", sizes)

    
    def set_fill_colors(self, fill_colors):
        """
        Set fill colors
        
        Parameters:

          fill_colors:
        
            Points fill color (vec4)
        """
        self.set_variable("fill_colors", fill_colors)

    def set_line_colors(self, line_colors):
        """
        """
        self.set_variable("line_colors", line_colors)
    
    def set_line_widths(self, line_widths):
        
        self.set_variable("line_widths", line_widths)

        
    def render(self, transform : Transform = None):
        """
        Render the visual using given transform

        Parameters:

          transform:
        
            Model/view/projection transform to use
        """

        # This rendering function could be further optimized when
        # positions/fill_colors/etc are all in a structured array.
        # Instead of doing indexing for each array, this could be made
        # only once.

        # Update transform
        if transform is not None:
            self._transform.set_data(transform)

        # Transform positions
        positions = self.get_attribute("positions")
        if self.is_transform("positions"):
            positions = positions.evaluate(self._uniforms, self._attributes)
        else:
            positions = np.asanyarray(positions)
        positions = positions.reshape(-1,3)
        positions = self._transform(positions) * (1,1,-1)
        indices = np.argsort(positions[:,2])
        positions = positions[indices]
        self._scatter.set_offsets(positions[:,:2])
    
        self.set_attribute("index", indices)
        self.set_attribute("screen", positions)

        # Set attributes
        if (fill_colors := self.eval_variable("fill_colors")) is not None:
            self._scatter.set_facecolors(fill_colors)
        if (line_colors := self.eval_variable("line_colors")) is not None:
            self._scatter.set_edgecolors(line_colors)
        if (line_widths := self.eval_variable("line_widths")) is not None:
            self._scatter.set_linewidths(line_widths)
        if (sizes := self.eval_variable("sizes")) is not None:
            self._scatter.set_sizes(sizes)
            
        # self._initialized becomes true after first rendering
        self._initialized = True
