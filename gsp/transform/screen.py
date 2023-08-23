# -----------------------------------------------------------------------------
# Graphic Server Protocol (GSP) — matplotlib backend
# Copyright 2023 Vispy Development Team - BSD 2 Clauses licence
# -----------------------------------------------------------------------------
from gsp.transform import Transform

class Screen(Transform):

    def __init__(self, buffer="positions"):
        """
        Screen transform is a JIT transform that return screen
        coordinates (including depth)
        """
        
        Transform.__init__(self)
        self._buffer = buffer

    def __call__(self):
        raise ValueError("Depth transform cannot be composed")
        
    def evaluate(self, buffers):
        if "screen" in buffers.keys():
            if self._buffer in buffers["screen"].keys():
                return buffers["screen"][self._buffer]
            else:
                raise ValueError(f"Screen buffer for {self._buffer} not found")
        else:
            raise ValueError("Screen buffer not found")
    
class ScreenX(Screen):
    """
    ScreenX transform is a JIT transform that return x screen coordinates.
    """
    def evaluate(self, buffers):
        return super().evaluate(buffers)[..., 0]

class ScreenY(Screen):
    """
    ScreenY transform is a JIT transform that return y screen coordinates.
    """
    def evaluate(self, buffers=None):
        return super().evaluate(buffers)[..., 1]
    
class ScreenZ(Screen):
    """
    ScreenZ transform is a JIT transform that return z (depth)
    screen coordinates.
    """
    def evaluate(self, buffers):
        return super().evaluate(buffers)[..., 2]
