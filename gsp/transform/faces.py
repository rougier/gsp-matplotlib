# -----------------------------------------------------------------------------
# Graphic Server Protocol (GSP) — matplotlib backend
# Copyright 2023 Vispy Development Team - BSD 2 Clauses licence
# -----------------------------------------------------------------------------
from gsp.transform import Transform

class Faces(Transform):

    def __init__(self):
        Transform.__init__(self)

    def __call__(self):
        raise ValueError("Faces transform cannot be composed")
        
    def evaluate(self, buffers=None):
        if "faces" in buffers.keys():
            return buffers["faces"]
        else:
            raise ValueError("Faces buffer not found")
