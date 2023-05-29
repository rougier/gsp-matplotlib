# -----------------------------------------------------------------------------
# Graphic Server Protocol (GSP) — matplotlib backend
# Copyright 2023 Vispy Development Team - BSD 2 Clauses licence
# -----------------------------------------------------------------------------
from gsp.transform import Transform

class Screen(Transform):

    def __init__(self):
        """
        Screen transform is a JIT transform that return screen
        coordinates (including depth)
        """
        
        Transform.__init__(self)

    def is_jit(self):
        """
        Indicate whether transform is a JIT transform
        """
        return True

    def __call__(self):
        raise ValueError("Depth transform cannot be composed")
        
    def evaluate(self, uniforms, attributes):
        return attributes["screen"]

class ScreenX(Screen):
    """
    ScreenX transform is a JIT transform that return x screen coordinates.
    """
    def evaluate(self, uniforms, attributes):
        buffer = super().evaluate(uniforms, attributes)
        return buffer[..., 0]

class ScreenY(Screen):
    """
    ScreenY transform is a JIT transform that return y screen coordinates.
    """
    def evaluate(self, buffers=None):
        buffer = super().evaluate(uniforms, attributes)
        return buffer[..., 1]
    
class ScreenZ(Screen):
    """
    ScreenZ transform is a JIT transform that return z (depth)
    screen coordinates.
    """
    def evaluate(self, uniforms, attributes):
        buffer = super().evaluate(uniforms, attributes)
        return buffer[..., 2]

class Depth(Screen):
    """
    Depth transform is a JIT transform that return z (depth)
    screen coordinates.
    """
    def evaluate(self, uniforms, attributes):
        return attributes["depth"]

        
