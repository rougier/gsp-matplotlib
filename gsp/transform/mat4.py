# -----------------------------------------------------------------------------
# Graphic Server Protocol (GSP) — matplotlib backend
# Copyright 2023 Vispy Development Team - BSD 2 Clauses licence
# -----------------------------------------------------------------------------
import numpy as np
from gsp.glm import mat4
from gsp.core import Buffer
from gsp.transform import Transform

class Mat4(Transform):

    def __init__(self, data : bytes):
        Transform.__init__(self)
        self._data = np.frombuffer(data, dtype=np.float32).view(mat4)

    def set_data(self, data):
        self._data[...] = np.frombuffer(data, np.float32)
        
    def __call__(self, V):

        M = self._data.reshape(4,4)

        #V = np.asarray(V, dtype=np.float32)
        shape = V.shape
        V = V.reshape(-1,3)
        ones = np.ones(len(V), dtype=np.float32)
        V = np.c_[V.astype(np.float32), ones]  # Homogenous coordinates
        V = V @ M.T                   # Transformed coordinates
        V = V/V[:,3].reshape(-1,1)             # Normalization
        V = V[:,:3]                            # Normalized device coordinates

        return V.reshape(shape)
