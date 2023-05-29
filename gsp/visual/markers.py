# -----------------------------------------------------------------------------
# Graphic Server Protocol (GSP)
# Copyright 2023 Vispy Development Team - BSD 2 Clauses licence
# -----------------------------------------------------------------------------
import numpy as np
import matplotlib as mpl
from gsp.visual import Visual
from gsp.transform import Transform
from gsp.core import Viewport, Buffer, Color, Measure, Marker

class Markers(Visual):
    def __init__(self, viewport :    Viewport,
                       positions :   Transform | Buffer,
                       types :       Transform | Buffer | Marker  = Marker.point,
                       sizes :       Transform | Buffer | Measure = 25.0,
                       angles :      Transform | Buffer | Measure = 0.0,
                       fill_colors : Transform | Buffer | Color   = Color(0,0,0,1),
                       line_colors : Transform | Buffer | Color   = Color(0,0,0,1),
                       line_widths : Transform | Buffer | Measure = 0):
        """
        Collection of markers with type, size and colors.

        Parameters:

          viewport:

            Viewport where this visual will be rendered
        
          positions:
        
            Marker position (vec3)

          types:
        
            Marker type (scalar)

          sizes:
        
            Marker size (scalar)

          angles:
        
            Marker rotation in radians (scalar)

          fill_colors:
        
            Points fill color (vec4)

          line_colors:
        
            Points line color (vec4)

          line_widths:
        
            Points line widths (scalar)
        """
        
        Visual.__init__(self, viewport)

        self.set_attribute("positions", positions)
        self.set_variable("sizes", sizes)
        self.set_variable("types", types)
        self.set_variable("angles", angles)
        self.set_variable("fill_colors", fill_colors)
        self.set_variable("line_colors", line_colors)
        self.set_variable("line_widths", line_widths)

        kwargs = {}
        if self.is_uniform("size"):
            kwargs["s"] = sizes
        if self.is_uniform("types"):
            kwargs["marker"] = types
        if self.is_uniform("line_widths"):
            kwargs["linewidth"] = line_widths
        if self.is_uniform("fill_colors"):
            kwargs["facecolors"] = fill_colors
        if self.is_uniform("line_colors"):
            kwargs["edgecolors"] = line_colors

        self._scatter = self._viewport._axes.scatter( [],[], **kwargs)
        self._scatter.set_visible(True)
        self._scatter.set_antialiaseds(True)
        
        # canvas = self._viewport._canvas._figure.canvas
        # canvas.mpl_connect('resize_event', lambda event: self.render())


    def render(self, transform : Transform = None):
        """
        Render the visual using given transform

        Parameters:

          transform:
        
            Model/view/projection transform to use
        """

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
        types = self.eval_variable("types")
        angles = self.eval_variable("angles")
        if self.is_attribute("types") or self.is_attribute("angles"):
            paths = []
            for i in range(len(positions)):
                try:
                    mtype = types[i]
                except:
                    mtype = types
                try:
                    angle = angles[i]
                except:
                    mtype = angles
                mtype = Marker.path(mtype)
                marker = mpl.markers.MarkerStyle(mtype)
                rotation = mpl.transforms.Affine2D().rotate_deg(angle)
                transform = marker.get_transform() + rotation
                path = marker.get_path().transformed(transform)

                # V = np.asarray(path._vertices)
                # zeros = np.zeros(len(V), dtype=np.float32)
                # V = np.c_[V.astype(np.float32), zeros]
                # V = self._transform(V)
                # path._vertices = V[:,:2]
                
                paths.append(path)
            self._scatter.set_paths(paths)

        if (fill_colors := self.eval_variable("fill_colors")) is not None:
            self._scatter.set_facecolors(fill_colors)
        if (line_colors := self.eval_variable("line_colors")) is not None:
            self._scatter.set_edgecolors(line_colors)
        if (line_widths := self.eval_variable("line_widths")) is not None:
            self._scatter.set_linewidths(line_widths)
        if (sizes := self.eval_variable("sizes")) is not None:
            self._scatter.set_sizes(sizes)

            
