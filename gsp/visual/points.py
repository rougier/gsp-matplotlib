# -----------------------------------------------------------------------------
# Graphic Server Protocol (GSP)
# Copyright 2023 Vispy Development Team - BSD 2 Clauses licence
# -----------------------------------------------------------------------------
import numpy as np
from gsp import glm
from gsp.visual import Visual
from gsp.core import Viewport, Buffer, Color, Measure


class Points(Visual):
    """
    !!! Note "Quick documentation"
    
        === "Definition"

            ![](../../assets/simple-points.png){ width="33%" align=right }

            Points are discs with a given size (diameter) and posses a
            surface that can be filled and stroked. They always face the
            viewer such that their rendered shape is a disc,
            independentely of any transform.

        === "Code example"

            ```python
            import numpy as np
            import matplotlib.pyplot as plt
            from gsp import glm, core, visual, transform

            canvas = core.Canvas(512, 512, 100.0)
            viewport = core.Viewport(canvas,0,0,512,512)
            camera = glm.Camera("ortho")

            n = 600
            P = glm.vec3(n)
            P.x = np.linspace(0.05,0.95,n)
            P.xy = np.linspace(0,10.125*2*np.pi,n)
            sizes = np.linspace(0.05, 12.0,n)**2
            points = visual.Points(P, sizes)
            points.render(viewport, camera.transform)
            plt.show()
            ```
    """

    def __init__(self, positions,
                       sizes = 25.0,
                       fill_colors = Color(0,0,0,1),
                       line_colors = Color(0,0,0,1),
                       line_widths = 0):
        """
        Create a visual of n points at given *positions* with
        given *sizes*, *flll_colors*., *line_colors* and
        *line_widths*.

        Parameters
        ----------
        positions : Transform | Buffer
            Points position (vec3)
        sizes : Transform | Buffer | Measure
            Point sizes (float)
        fill_colors : Transform | Buffer | Color
            Points fill colors (vec4)
        line_colors : Transform | Buffer | Color
            Points line colors (vec4)
        line_widths : Transform | Buffer | Measure
            Points line colors (vec4)
        """

        Visual.__init__(self)
        self.set_variable("positions", positions)
        self.set_variable("sizes", sizes)
        self.set_variable("fill_colors", fill_colors)
        self.set_variable("line_colors", line_colors)
        self.set_variable("line_widths", line_widths)
        
        
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
        
        transform = proj @ view @ model
        self.set_variable("viewport", viewport)
        
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
        positions = positions.reshape(-1,3)
        positions = glm.to_vec3(glm.to_vec4(positions) @ transform.T)
        depth = -positions[:,2]
        
        sort_indices = np.argsort(depth)
        positions = positions[sort_indices]
        collection.set_offsets(positions[:,:2])
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
            
