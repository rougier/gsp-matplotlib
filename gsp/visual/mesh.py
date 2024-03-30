# Package: Graphic Server Protocol / Matplotlib
# Authors: Nicolas P .Rougier <nicolas.rougier@inria.fr>
# License: BSD 3 clause
import numpy as np
from gsp import glm
from gsp.visual import Visual
from matplotlib.collections import PolyCollection
from gsp.core import Viewport, Buffer, Color, Measure

class Mesh(Visual):
    """
    !!! Note "Quick documentation"

        === "Definition"

            ![](../../assets/simple-mesh.png){ width="33%" align=right }

            Meshes are collection of triangles that can be filled, stroked
            and textured.


        === "Code example"

             ```python
             import numpy as np
             import matplotlib.pyplot as plt
             from gsp import glm, core, visual, transform

             canvas   = core.Canvas(512, 512, 100.0)
             viewport = core.Viewport(canvas, 0, 0, 512, 512)
             camera   = glm.Camera("perspective", theta=-20, phi=2.5)

             V,Vi = glm.mesh("data/bunny-4096.obj")
             EC = core.Color(0.00, 0.00, 0.00, 1.00)
             FC = core.Color(1.00, 1.00, 1.00, 0.85)
             mesh = visual.Mesh(V, Vi, None, FC, EC, 0.25)
             mesh.render(viewport, camera.model, camera.view, camera.proj)

             camera.connect(viewport, "motion",  mesh.render)
             plt.show()
             ```
    """


    def __init__(self, positions, face_indices,
                       line_indices = None,
                       fill_colors = Color(1,1,1,1),
                       line_colors = Color(0,0,0,1),
                       line_widths = 0):
        """
        Create a visual for one or several meshes using *positions* and
        *face_indices* (that describes triangles) and *line_indices*
        (that describes paths). Each triangle can be painted with
        *fill_colors* and paths can be stroke using *line_colors* and
        *line_widths*.

        !!! Note "Notes on matplotlib implementation"

            - Line indices are not used and lines always correspond to
              triangles edges. We could use an additional path
              collection for rendering lines but the, we could not
              sort paths/triangles accross the two collections.

            - Fill colors are always related to faces because
              matplotlib does not implement barycentric interpolation
              inside a triangle.

        Parameters
        ----------
        positions : Transform | Buffer
            Vertices positions (vec3)
        face_indices : Transform | Buffer
            Face indices (int)
        line_indices :  Transform | Buffer | None
            Line indices (int)
        fill_colors : Transform | Buffer | Color
            Faces color (vec4)
        line_colors : Transform | Buffer | Color
            Line colors (vec4)
        line_widths : Transform | Buffer | Measure
            Line widths (scalar)
        """

        Visual.__init__(self)
        self.set_variable("positions", positions)
        self.set_variable("face_indices", face_indices)
        self.set_variable("fill_colors", fill_colors)
        self.set_variable("line_colors", line_colors)
        self.set_variable("line_widths", line_widths)


    def render(self, viewport, model=None, view=None, proj=None):
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

        if viewport not in self._viewports:
            collection = PolyCollection([], clip_on=True, snap=False)
            self._viewports[viewport] = collection
            viewport._axes.add_collection(collection, autolim=False)

            # This is necessary for measure transforms that need to be
            # kept up to date with canvas size
            canvas = viewport._canvas._figure.canvas
            canvas.mpl_connect('resize_event',
                               lambda event: self.render(viewport))

        collection = self._viewports[viewport]

        # Get positions
        positions = self.eval_variable("positions")
        positions = positions.reshape(-1,3)

        # Get face indices as triangles
        face_indices = self.eval_variable("face_indices")
        face_indices = face_indices.reshape(-1,3)

        # Compute tranformed triangles (faces) and their (mean) depth
        positions = glm.to_vec3(glm.to_vec4(positions) @ transform.T)
        p_depth = positions[:,2]
        faces = positions[face_indices]
        f_depth = -faces[:,:,2].mean(axis=1)

        self.set_variable("screen", {"positions": positions,
                                   "faces": faces} )
        self.set_variable("depth",  {"positions": p_depth,
                                   "faces": f_depth} )

        # Sort faces according to f_depth
        sort_indices = np.argsort(f_depth)


        # Set positions in the collection
        collection.set_verts(faces[sort_indices,:,:2])

        # Set fill color(s)
        fill_colors = self.eval_variable("fill_colors")
        if isinstance(fill_colors, np.ndarray) and (len(fill_colors) == len(faces)):
            collection.set_facecolors(fill_colors[sort_indices,:])
        else:
            collection.set_facecolors(fill_colors)

        # Set line color(s)
        line_colors = self.eval_variable("line_colors")
        if line_colors is not None:
            if isinstance(line_colors, np.ndarray) and (len(line_colors) == len(faces)):
                collection.set_edgecolors(line_colors[sort_indices,:])
            else:
                collection.set_edgecolors(line_colors)

        # Set line width(s)
        line_widths = self.eval_variable("line_widths")
        if line_widths is not None:
            collection.set_linewidths(line_widths)
            collection.set_antialiaseds(line_widths > 0)
