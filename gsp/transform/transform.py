# -----------------------------------------------------------------------------
# Graphic Server Protocol (GSP)
# Copyright 2023 Vispy Development Team - BSD 2 Clauses licence
# -----------------------------------------------------------------------------
from __future__ import annotations

import numpy as np
from gsp.core import Buffer

class Transform:

    def __init__(self, base = None,
                       next = None,
                       buffer = None):
        """
        A Transform allows to apply an arbitratry transformation to
        a buffer. Any transform can be bound to a specific buffer and
        used in place of a Buffer where needed. Several transforms can
        be chained or composed together.

        Parameters
        ----------
        base : Transform
            The base transform this transform is based on. When non
            null, all transform parameters are read from the base.
        next : Transform
            A transformation can be chained with another transform
            (`next`). In such case, the **`next` transform is applied
            first** and result is passed to the current transform.
        buffer : Buffer
            Buffer on which to apply the transform. When non null, the
            transformation is bound and cannot be modified anymore.
        """
        self._base = base
        self._next = next
        self._buffer = buffer

    def set_base(self, base = None):
        """
        Set a new base for the transform

        Parameters
        ----------
        base : Transform
            The base transform this transform is based on
        """

        self._base = base

    def set_next(self, next = None):
        """
        Compose transform with `next` that will be applied before
        this one.

        Parameters
        ----------
        next : Transform
            Next transform
        """

        self._next = next

    def set_buffer(self, buffer = None):
        """Bind the transform to the given buffer.

        Parameters
        ----------
        buffer : Buffer
            Buffer to bind
        """

        self._buffer = buffer

    def evaluate(self, buffer):
        """
        Evaluate the transform

        Parameters
        ----------
        buffer : Buffer
            Buffer to bind
        """

        raise NotImplementedError("Generic transforms cannot be evaluated")

    @property
    def base(self):
        """
        The base transform this transform is based on
        """

        if self._base:
            return self._base.base
        return self

    @property
    def buffer(self):
        """
        Buffer on which to apply the transform.
        """

        return self._buffer

    @property
    def next(self):
        """
        The next transform in the chain of transforms
        """

        return self._next

    @property
    def last(self):
        """
        The last transform in the chain of transforms
        """

        last = self
        while last._next: last = last._next
        return last

    @property
    def bound(self):
        """
        Indicate if this transform is bound
        """
        return self.last.buffer is not None

    def copy(self):
        """
        Copy the transform
        """

        transform = self.__class__()
        transform.set_buffer(self._buffer)
        transform.set_base(self.base)
        if self._next:
            transform.set_next(self._next.copy())
        return transform

    def __call__(self, other):
        """
        Chain (Transform) or bind (Buffer) self and other.
        """

        transform = self.copy()
        if isinstance(other, Transform):
            transform.set_next(other.copy())
            transform.set_buffer(None)
        elif isinstance(other, (Buffer, np.ndarray, float, int, tuple)):
            if self.bound:
                raise ValueError("Transform is already bound")
            transform.last.set_buffer(other)
        else:
            raise ValueError("Unknown type")
        return transform

    def __add__(self, other):
        from gsp.transform import Add
        return Add(self, other)

    def __radd__(self, other):
        from gsp.transform import Add
        return Add(self, other)

    def __sub__(self, other):
        from gsp.transform import Sub
        return Sub(self, other)

    def __rsub__(self, other):
        from gsp.transform import Sub
        return Sub(other, self)

    def __mul__(self, other):
        from gsp.transform import Mul
        return Mul(self, other)

    def __div__(self, other):
        from gsp.transform import Div
        return Div(self, other)
