# -----------------------------------------------------------------------------
# Graphic Server Protocol (GSP)
# Copyright 2023 Vispy Development Team - BSD 2 Clauses licence
# -----------------------------------------------------------------------------
import numpy as np
from gsp.core import Viewport, Buffer
from gsp.glm import mat4, tracked_array
from gsp.transform import Mat4, Transform

class Visual:
    def __init__(self, viewport : Viewport):
        """
        Generic visual

        Parameters:

          viewport:

            Viewport where this visual will be rendered
        """
        
        self._viewport = viewport
        self._initialized = False
        self._transform = Mat4(mat4())

        # Uniforms are per-primitive parameters (constant during an
        # entire render call)
        self._uniforms  = {
            "viewport" :   self._viewport,
            "model" :      None,
            "view" :       None,
            "projection" : None 
        }
        
        # Attributes are per-vertex parameters (typically : positions,
        # normals, colors, etc)
        self._attributes = {
            "screen" : None,
            "index"  : None,
            "normal" : None
        }
        
        canvas = self._viewport._canvas._figure.canvas
        canvas.mpl_connect('resize_event', lambda event: self.render())

    def is_transform(self, name):
        """Check if a variable is a transform"""
        
        if self.is_uniform(name):
            return isinstance(self._uniforms[name], Transform)
        elif self.is_attribute(name):
            return isinstance(self._attributes[name], Transform)
        else:
            raise IndexError(f"Unknown variable ({name})")
    
    def is_variable(self, name):
        """Test wheter name is a variable (uniform or attribute)"""
        return self.is_uniform(name) or self.is_attribute(name)
        
    def is_uniform(self, name):
        """Test wheter name is a uniform"""
        return name in self._uniforms.keys()

    def is_attribute(self, name):
        """Test wheter name is an attribute"""
        return name in self._attributes.keys()
        
    def set_variable(self, name, value):
        """Store value as a uniform or attribute"""
        
        if isinstance(value, Transform):
            if value.is_jit():
                self.set_attribute(name, value)
            else:
                last = value.last.buffer
                if not hasattr(last, "__len__") or len(last) == 1:
                    self.set_uniform(name, value)
                else:
                    self.set_attribute(name, value)
                    
        elif isinstance(value, (Buffer, np.ndarray)):
            if not hasattr(value, "__len__") or len(value) == 1:
                self.set_uniform(name, value)
            else:
                self.set_attribute(name, value)
        else:
            self.set_uniform(name, value)

    def set_uniform(self, name, value):
        """Store value as a uniform"""
        if name in self._attributes.keys():
            del self._attributes[name]
        self._uniforms[name] = value
                
    def set_attribute(self, name, value):
        """Store value as an attribute"""
        if name in self._uniforms.keys():
            del self._uniforms[name]
        self._attributes[name] = value

        
    def get_variable(self, name):
        """
        Get a variable
        """
        
        if self.is_uniform(name):
            return self._uniforms[name]
        elif self.is_attribute(name):
            return self._attributes[name]
        else:
            raise IndexError(f"Unknown variable ({name})")

    def get_uniform(self, name):
        """
        Get a uniform variable
        """
        
        if self.is_uniform(name):
            return self._uniforms[name]
        else:
            raise IndexError(f"Unknown variable ({name})")

    def get_attribute(self, name):
        """
        Get an attribute variable
        """
        
        if self.is_attribute(name):
            return self._attributes[name]
        else:
            raise IndexError(f"Unknown variable ({name})")

        
    def eval_variable(self, name):
        """
        Eval and return a variable
        """
        
        if self.is_uniform(name):
            return self.eval_uniform(name)
        elif self.is_attribute(name):
            return self.eval_attribute(name)
        else:
            raise IndexError(f"Unknown variable ({name})")

    def eval_uniform(self, name):
        """
        Eval and return a uniform
        """
        
        uniform = self._uniforms[name]                
        if isinstance(uniform, Transform):
            value = uniform.evaluate(self._uniforms, self._attributes)
        else:
            value = np.asanyarray(uniform)
        return np.atleast_1d(value)
            
        
    def eval_attribute(self, name):
        """
        Eval and return an attribute
        """
        
        index = self._attributes["index"]
        attribute = self._attributes[name]
        if isinstance(attribute, Transform):
            output = attribute.evaluate(self._uniforms, self._attributes)
        elif isinstance(attribute, (Buffer,np.ndarray)):
            output = np.asanyarray(attribute)
            if index is not None and len(attribute) == len(index):
                output = output[index]
        else:
            output = np.asanyarray(attribute)
        return np.atleast_1d(output)


    def render(self, transform : Transform = None):
        """
        Render the visual using given transform

        Parameters:

          transform:
        
            Transform to use
        """

        raise NotImplemented
