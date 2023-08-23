# -----------------------------------------------------------------------------
# Graphic Server Protocol (GSP) — matplotlib backend
# Copyright 2023 Vispy Development Team - BSD 2 Clauses licence
# -----------------------------------------------------------------------------
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
