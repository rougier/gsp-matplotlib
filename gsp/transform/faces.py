# Package: Graphic Server Protocol / Matplotlib
# Authors: Nicolas P .Rougier <nicolas.rougier@inria.fr>
# License: BSD 3 clause
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
