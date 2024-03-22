# -----------------------------------------------------------------------------
# Graphic Server Protocol (GSP)
# Copyright 2023 Vispy Development Team - BSD 2 Clauses licence
# -----------------------------------------------------------------------------
import numpy as np
import matplotlib as mpl
from gsp import glm
from gsp.visual import Visual
from gsp.transform import Transform
from gsp.core import Viewport, Buffer, Color, Measure, Marker

class Markers(Visual):
    """
    !!! Note "Quick documentation"

        === "Definition"

            ![](../../assets/simple-markers.png){ width="33%" align=right }

            Markers are arbitrary two-dimensional polygons
            (including discs) with a given size that possess a surface
            that can be filled and stroked. They are flat but can be
            oriented towards any direction in space.

        === "Code example"

             ```python
             import numpy as np
             import matplotlib.pyplot as plt
             from gsp import core, visual, transform, glm

             canvas   = core.Canvas(512, 512, 100.0)
             viewport = core.Viewport(canvas, 0, 0, 512, 512)
             camera   = glm.Camera("ortho")

             n = 200
             V = np.zeros(n, [ ("position", np.float32, 3),
                               ("size",     np.float32),
                               ("angle",    np.float32),
                               ("type",     np.float32),
                               ("color",    np.float32, 4) ])
             R = np.linspace(0.25, 0.95, n)
             T = np.linspace(0, 10.125*2*np.pi, n)
             V["position"][:,0] = R*np.cos(T)
             V["position"][:,1] = R*np.sin(T)
             V["size"] = np.linspace(10, 20, n)**2
             V["angle"] = 180*T/np.pi - 90
             V["type"] = [core.Marker.heart, core.Marker.club,
                          core.Marker.diamond, core.Marker.spade]*(n//4)
             V["color"] = [(1,0,0,1), (0,0,0,1), (1,0,0,1), (0,0,0,1)]*(n//4)
             black, white = core.Color(0,0,0,1), core.Color(0,0,0,1)

             points = visual.Markers(V["position"], V["type"], V["size"],
                                     V["angle"], V["color"], black, 0)
             points.render(viewport, camera.transform)
             plt.show()
             ```
    """
        
    def __init__(self, positions,
                       types = Marker.point,
                       sizes = 25.0,
                       axis = None,
                       angles = 0.0,
                       fill_colors = Color(0,0,0,1),
                       line_colors = Color(0,0,0,1),
                       line_widths = 0):
        """
        Create a visual of n markers at given *positions* with
        given *types*, *sizes*, *flll_colors*., *line_colors* and
        *line_widths*. Markers can oriented individually along a given
        *axis* and *angles*.

        Parameters
        ----------
        positions : Transform | Buffer
            Markers position (vec3)
        types : Transform | Buffer | Marker
            Markers types (marker)
        sizes : Transform | Buffer | Measure
            Markers sizes (float)
        axis : Transform | Buffer | None
            Markers vertical axis (vec3)
        angles: Transform | Buffer | Measure
            Makers' angle aroudn their axis (float)
        fill_colors : Transform | Buffer | Color
            Markers fill colors (vec4)
        line_colors : Transform | Buffer | Color
            Markers line colors (vec4)
        line_widths : Transform | Buffer | Measure
            Markers line colors (vec4)
        """
        
        Visual.__init__(self)
        self.set_variable("positions", positions)
        self.set_variable("sizes", sizes)
        self.set_variable("types", types)
        self.set_variable("axis", axis)
        self.set_variable("angles", angles)
        self.set_variable("fill_colors", fill_colors)
        self.set_variable("line_colors", line_colors)
        self.set_variable("line_widths", line_widths)
        self.generate_markers(positions)


    def generate_markers(self, positions):
        """
        Generate paths for markers and dependng on positions.
        """
        
        axis = self.eval_variable("axis")
        types = self.eval_variable("types")
        angles = self.eval_variable("angles")
        self.paths = None

        # If types or angles are set individually, we need to generate paths
        if (axis is not None or
            (hasattr(types, "__len__") and len(types) == len(positions)) or
            (hasattr(angles, "__len__") and len(angles) == len(positions))):
            self.paths = []
            for i in range(len(positions)):
                try:    mtype = types[i]
                except: mtype = types
                try:    angle = float(angles[i])
                except: angle = float(angles)
                try:    axis = axis[i]
                except: axis = axis
                
                mtype = Marker.path(mtype)
                marker = mpl.markers.MarkerStyle(mtype)
                transform = marker.get_transform()
                path = marker.get_path().transformed(transform)

                transform = glm.zrotate(angle)
                if axis is not None:
                    z_axis = (0,0,1)
                    A = glm.align(positions[i], z_axis)
                    transform = A @ transform                    
                V = np.asarray(path._vertices, dtype=np.float32)
                zeros = np.zeros(len(V), dtype=np.float32)
                ones = np.ones(len(V), dtype=np.float32)
                Z = np.c_[V, zeros, ones]
                Z = Z @ transform.T
                # Z = Z / Z[3]
                path._vertices = Z[:,:2]                
                self.paths.append(path)
        

    def render(self, viewport=None, model=None, view=None, proj=None):
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

        self.set_variable("viewport", viewport)
        transform = proj @ view @ model

        # Create the collection if necessary
        if viewport not in self._viewports:
            collection = viewport._axes.scatter([],[])
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
        
        axis = self.eval_variable("axis")
        if axis is not None:
            P = glm.to_vec3(glm.to_vec4(positions) @ model.T)
            self.generate_markers(P)

        positions = glm.to_vec3(glm.to_vec4(positions) @ transform.T)
        depth = -positions[:,2]

        sort_indices = np.argsort(depth)
        positions = positions[sort_indices]
        collection.set_offsets(positions[:,:2])

        if axis is not None:
            paths = [self.paths[i] for i in sort_indices]
            collection.set_paths(paths)

        self.set_variable("screen", {"positions": positions})
        self.set_variable("depth",  {"positions": depth})


        fill_colors = self.eval_variable("fill_colors")
        if isinstance(fill_colors, np.ndarray) and (len(fill_colors) == len(positions)):
            collection.set_facecolors(fill_colors[sort_indices])
        else:
            collection.set_facecolors(fill_colors)

        line_colors = self.eval_variable("line_colors")
        if isinstance(line_colors, np.ndarray) and (len(line_colors) == len(positions)):
            collection.set_edgecolors(line_colors[sort_indices])
        else:
            collection.set_edgecolors(line_colors)

        line_widths = self.eval_variable("line_widths")
        if isinstance(line_widths, np.ndarray) and (len(line_widths) == len(positions)):
            collection.set_linewidths(line_widths[sort_indices])
        else:
            collection.set_linewidths(line_widths)

        sizes = self.eval_variable("sizes")
        if isinstance(sizes, np.ndarray) and (len(sizes) == len(positions)):
            collection.set_sizes(sizes[sort_indices])
        else:
            collection.set_sizes(sizes)

            
