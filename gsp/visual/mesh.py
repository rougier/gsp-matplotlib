# -----------------------------------------------------------------------------
# Graphic Server Protocol (GSP)
# Copyright 2023 Vispy Development Team - BSD 2 Clauses licence
# -----------------------------------------------------------------------------
import numpy as np
from gsp.glm import mat4
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
from gsp.transform import Transform, Mat4
from gsp.core import Viewport, Buffer, Color, Measure
from gsp.visual import Visual

class Mesh(Visual):
    def __init__(self, viewport : Viewport,
                       positions: Transform | Buffer,
                       indices : Transform | Buffer,
                       fill_colors : Transform | Buffer | Color   = Color(1,1,1,1),
                       line_colors : Transform | Buffer | Color   = Color(0,0,0,1),
                       line_widths : Transform | Buffer | Measure = 0,
                       shading : str = "flat"):
        """
        Mesh as a collection of triangles

        Parameters:

          viewport:
        
            Viewport where this visual will be renderdd

          positions:
        
            Vertices positions (vec3)

          indices:
        
            Indices of triangles (vec3)

          fill_colors:
        
            Triangles fill color (vec4)

          line_colors:
        
            Triangles line color (vec4)

          line_widths:
        
            Triangles line widths (scalar)
        
          shading_mode:
        
            Flat, Gouraud or Phong
        
        """

        Visual.__init__(self, viewport)
        self._shading = shading

        self.set_attribute("positions", positions)
        self.set_attribute("indices", indices)
        self.set_variable("fill_colors", fill_colors)
        self.set_variable("line_colors", line_colors)
        self.set_variable("line_widths", line_widths)
        
        self._collection = PolyCollection([], clip_on=True, snap=False)
        self._viewport._axes.add_collection(self._collection, autolim=False)


    def render(self, transform : Transform = None,
                     mode : str = None):
        """
        Render the visual using given transform

        Parameters:

          transform:
        
            Model/view/projection transform to use

          mode :

            Render mode, one of None, "front" or "back"
        """


        # Update transform
        if transform is not None:
            self._transform.set_data(transform)


        # Get positions
        positions = self.get_attribute("positions")
        if self.is_transform("positions"):
            positions = positions.evaluate(self._uniforms, self._attributes)
        else:
            positions = np.asanyarray(positions)
        positions = positions.reshape(-1,3)

        # Get indices
        indices = self.get_attribute("indices")
        if self.is_transform("indices"):
            indices = indices.evaluate(self._uniforms, self._attributes)
        else:
            indices = np.asanyarray(indices)
        indices = indices.reshape(-1,3)

        # Compute tranformed triangles (T) and their (mean) depth (Z)
        T = self._transform(positions)[indices]
        Z = -T[:,:,2].mean(axis=1)

        # Check which mode to use (front, back or both)
        index = None
        if mode == "front":
            index, _ = glm.frontback(T)
            T, Z = T[index], Z[index]
        elif mode == "back":
            _, index = glm.frontback(T)
            T, Z = T[index], Z[index]

        self.set_attribute("screen", T)
        self.set_attribute("depth", Z)
        self.set_attribute("index", index)
            
        # Get 2d triangles
        T = T[:,:,:2]
        
        # Sort triangles according to z buffer
        I = np.argsort(Z)

        # Set positions
        self._collection.set_verts(T[I,:])
        
        # Set attributes
        fill_colors = self.eval_variable("fill_colors")
        if self.is_attribute("fill_colors"):
            self._collection.set_facecolors(fill_colors[I,:])
        else:
            self._collection.set_facecolors(fill_colors)

        line_colors = self.eval_variable("line_colors")
        if self.is_attribute("line_colors"):
            self._collection.set_edgecolors(line_colors[I,:])
        else:
            self._collection.set_edgecolors(line_colors)

        line_widths = self.eval_variable("line_widths")
        if line_widths is not None:
            self._collection.set_linewidths(line_widths)
            self._collection.set_antialiaseds(line_widths > 0)

