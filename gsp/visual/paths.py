# Package: Graphic Server Protocol / Matplotlib
# Authors: Nicolas P .Rougier <nicolas.rougier@inria.fr>
# License: BSD 3 clause
import glm
import numpy as np
from gsp.visual import Visual
from matplotlib.collections import LineCollection
from gsp.core import Viewport, Buffer, Color, Measure, LineCap, LineStyle, LineJoin


class Paths(Visual):
    """
    Paths are sequence of contiguous line segments passing through
    a series of vertices. They can be colored and styled (dash
    pattern). They possess a thickness but always face the viewer such
    that their apparent thickness is constant. Their end points (caps)
    can be styled following the SVG specification} (butt, round or
    cap). Their join can be styled following partially the SVG
    specification (round,
    miter, bevel).

    # Variables

    Considering a set of n paths and a total of N vertices, the size
    of each variable can be:

    ## Line color(s):

      - 1 : Paths have all the same uniform color (per visual)
      - n : Path have individual but uniform color (per item)
      - N : Path have per vertex colors with linear
                 interpolation between vertices (per vertex)

    ## Line width(s):

      - 1 : Paths have the same uniform width (per visual)
      - n : Path have individual but uniform width (per item)
      - N : Path have per vertex width with linear
            interpolation between vertices (per vertex)

    ## Line style(s):

      - 1 : Paths have the same style (per visual)
      - n : Paths have individual styles (per item)

    ## Line join(s):

      - 1 : Paths have all the same join style (per visual)
      - n : Paths have individual join style (per item)

    ## Line cap(s):

      - 1 : paths have all the same start & end cap (per visual)
      - 2 : paths have all the same start cap and the same
             end cap (start and end can be different) (per visual)
      - n : paths have individiual caps, start and end cap for
              a path are the same (per item)
      - 2n : paths have individiual caps, start and
              end cap for can be diffetent (per item)

    # Matplotlib implementation

    Matplotlib implementation has some limits regarding the level at
    which variables can be considered. Emulation is possible possible
    but is left to the responsability of the user.

    Variables      | per visual | per path | per vertex |
    ---------------|------------|----------|------------|
    `lines_colors` | yes        | yes︎︎      | no         |
    `lines_widths` | yes        | yes︎︎      | no         |
    `lines_styles` | yes        | yes      | --         |
    `lines_joins`  | yes        | no       | --         |
    `lines_caps`   | yes        | no       | --         |



        ```
    """

    def __init__(self, positions,
                       line_indices,
                       line_colors = Color(0,0,0,1),
                       line_widths = 1,
                       line_styles = LineStyle.solid,
                       line_caps = LineCap.round,
                       line_joins = LineJoin.round):
        """
        Create a visual of n paths at given positions with
        given line_colors, line_widths, lne_styles, line_caps
        and line_joins. A path is described by an orderd set of
        indices that refer to a set of positions.

        A visual can contains several paths when line_indices is a
        list of list of indices. These paths can be grouped when
        line_indices is a list of list of list.

        Parameters
        ----------
        positions : Transform | Buffer
            Points position
        line_indices : Transform | List
            Path vertex indices
        line_colors : Transform | Buffer | Color
            Points line colors
        line_widths : Transform | Buffer | Measure
            Points line widths
        line_styles : Transform | Buffer | LineStyle
            Points line colors
        line_caps : Transform | Buffer | LineCap
            Line caps
        line_joins : Transform | Buffer  | LineJoin
            Line joins
        """

        Visual.__init__(self)
        self.set_variable("positions", positions)
        self.set_variable("line_indices", line_indices)
        self.set_variable("line_colors", line_colors)
        self.set_variable("line_widths", line_widths)
        self.set_variable("line_styles", line_styles)
        self.set_variable("line_caps", line_caps)
        self.set_variable("line_joins", line_joins)


    def render(self, viewport=None, model=None, view=None, proj=None):
        """
        Render the visual on viewport using the given model, view,
        proj matrices.

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
            collection = LineCollection([], clip_on=True, snap=False)
            self._viewports[viewport] = collection
            viewport._axes.add_collection(collection, autolim=False)

            # This is necessary for measure transforms that need to be
            # kept up to date with canvas size
            canvas = viewport._canvas._figure.canvas
            canvas.mpl_connect('resize_event', lambda event: self.render(viewport))

        collection = self._viewports[viewport]
        positions = self.eval_variable("positions")
        positions = positions.reshape(-1,3)
        positions = glm.to_vec3(glm.to_vec4(positions) @ transform.T)
        positions = positions.reshape(-1,3)

        indices = self.eval_variable("line_indices").reshape(-1,2)
        paths = [positions[start:end+1] for (start,end) in indices]

        # We sort paths according to the mean depth of vertices composing the path
        # (we could used instead minimum or maximum depth among all the vertices)
        depth = [-p[...,2].mean() for p in paths]
        sort_indices = np.argsort(depth)

        paths = [paths[i][...,:2] for i in sort_indices]
        collection.set_paths(paths)
        self.set_variable("screen", {"positions": positions})
        self.set_variable("depth",  {"positions": positions[..., 2],
                                     "paths": depth})


        line_colors = self.eval_variable("line_colors")

        # Several colors
        if isinstance(line_colors, np.ndarray):
            # Number of color == number of paths
            if len(line_colors) == len(paths):
                collection.set_edgecolors(line_colors[sort_indices])
            # Number of colors == number of vertices
            elif len(line_colors) == len(positions):
                raise NotImplementedError("Per vertex line color is not available")
            else:
                collection.set_edgecolors(line_colors)
        # Unique line color
        else:
            collection.set_edgecolors(line_colors)


        line_widths = self.eval_variable("line_widths")

        # Several line_widths
        if isinstance(line_widths, np.ndarray):
            # Number of widths == number of paths
            if len(line_widths) == len(paths):
                collection.set_linewidths(line_widths[sort_indices])
            # Number of colors == number of vertices
            elif len(line_widths) == len(positions):
                raise NotImplementedError("Per vertex line widths is not available")
            else:
                collection.set_linewidths(line_widths)
        # Unique line width
        else:
            collection.set_linewidths(line_widths)


        if isinstance(line_widths, np.ndarray):
            # Number of caps == number of paths
            if len(line_widths) == len(paths):
                collection.set_linewidths(line_widths[sort_indices])
            # Number of colors == number of vertices
            elif len(line_widths) == len(positions):
                raise NotImplementedError("Per vertex line widths is not available")
            else:
                collection.set_linewidths(line_widths)
        # Unique line width
        else:
            collection.set_linewidths(line_widths)
