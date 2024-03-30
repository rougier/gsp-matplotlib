# Package: Graphic Server Protocol / Matplotlib
# Authors: Nicolas P .Rougier <nicolas.rougier@inria.fr>
# License: BSD 3 clause
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from gsp.core import Buffer
from gsp.transform import Transform

class Accessor(Transform):
    def __init__(self, buffer, key=None):
        Transform.__init__(self, buffer=buffer)
        self._key = key

    def copy(self):
        transform = Transform.copy(self)
        transform._key = self._key
        return transform

    def evaluate(self, buffers=None):
        if self._next:
            buffer = self._next.evaluate(buffers)
        elif self._buffer is not None:
            buffer = self._buffer
        else:
            raise ValueError("Transform is not bound")

        if buffer.dtype.names:
            buffer = buffer[self._key]
        elif self._key in "xyzw":
            buffer = buffer[..., "xyzw".index(self._key)]
        elif self._key in "rgba":
            buffer = buffer[..., "rgba".index(self._key)]
        else:
            raise IndexError(f"Unknown key {self._key}")

        if "index" in buffers.keys():
            return buffer[buffers["index"]]
        else:
            return buffer


class X(Accessor):
    def __init__(self, buffer=None):
        Accessor.__init__(self, buffer, "x")

class Y(Accessor):
    def __init__(self, buffer=None):
        Accessor.__init__(self, buffer, "y")

class Z(Accessor):
    def __init__(self, buffer=None):
        Accessor.__init__(self, buffer, "z")

class W(Accessor):
    def __init__(self, buffer=None):
        Accessor.__init__(self, buffer, "w")

class R(Accessor):
    def __init__(self, buffer=None):
        Accessor.__init__(self, buffer, "r")

class G(Accessor):
    def __init__(self, buffer=None):
        Accessor.__init__(self, buffer, "g")

class B(Accessor):
    def __init__(self, buffer=None):
        Accessor.__init__(self, buffer, "b")

class A(Accessor):
    def __init__(self, buffer=None):
        Accessor.__init__(self, buffer, "a")
