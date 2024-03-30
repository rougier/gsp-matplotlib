# Package: Graphic Server Protocol / Matplotlib
# Authors: Nicolas P .Rougier <nicolas.rougier@inria.fr>
# License: BSD 3 clause
from gsp.transform import Transform

class Depth(Transform):

    def __init__(self, buffer="positions"):
        Transform.__init__(self)
        self._buffer = buffer

    def __call__(self):
        raise ValueError("Depth transform cannot be composed")

    def evaluate(self, buffers):
        if "depth" in buffers.keys():
            if self._buffer in buffers["depth"].keys():
                return buffers["depth"][self._buffer]
            else:
                raise ValueError(f"Depth buffer for {self._buffer} not found")
        else:
            raise ValueError("Depth buffer not found")
