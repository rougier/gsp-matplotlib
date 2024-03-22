# -----------------------------------------------------------------------------
# Graphic Server Protocol (GSP)
# Copyright 2023 Vispy Development Team - BSD 2 Clauses licence
# -----------------------------------------------------------------------------
import numpy as np
from gsp.core import Viewport, Buffer
from gsp.transform import Transform

class Visual:
    def __init__(self):
        """ Generic visual """

        self._variables = {}
        self._viewports = {}

        self._model = np.eye(4)
        self._view = np.eye(4)
        self._proj = np.eye(4)

    def set_variable(self, name, value):
        """
        Store variable *name*

        Parameters
        ----------
        name : string
            Name of the variable to store
        value : any
            Value of the variable to store
        """
        self._variables[name] = value

    def get_variable(self, name):
        """
        Retrieve variable *name* (without evaluation)

        Parameters
        ----------
        name : string
            Name of the variable to retrieve
        """

        if name in self._variables.keys():
            return self._variables[name]
        raise IndexError(f"Unknown variable ({name})")

    def eval_variable(self, name):
        """
        Evaluate and return variable *name*

        Parameters
        ----------
        name : string
            Name of the variable to evaluate
        """

        value = self.get_variable(name)
        if isinstance(value, Transform):
            value = value.evaluate(self._variables)
        elif isinstance(value, (Buffer,np.ndarray)):
            value = np.asanyarray(value)
        return np.atleast_1d(value)

    def render(self, viewport, transform = None):
        """Render the visual on *viewport* using the given *transform*.

        Parameters
        ----------
        viewport : Viewport
            Viewport where to render the visual
        transform : Transform
            Transfrom matrix to use for rendering
        """

        self.set_variable("viewport", viewport)
        if transform is not None:
            self._transform.set_data(transform)
