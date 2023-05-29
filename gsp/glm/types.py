# -----------------------------------------------------------------------------
# Graphic Server Protocol (GSP)
# Copyright 2023 Vispy Development Team - BSD 2 Clauses licence
# -----------------------------------------------------------------------------
"""
Numpy helper objects to create GL compatible buffers, vectors and matrices.

- ctypes - list of types that can be used for scalars, vectors & matrices

- scalar_t(ctype) - scalar type constructor
- vec2_t(ctype) - vec2 type constructor
- vec3_t(ctype) - vec3 type constructor
- vec4_t(ctype) - vec4 type constructor

- mat2_t(ctype) - mat2 type constructor
- mat3_t(ctype) - mat3 type constructor
- mat4_t(ctype) - mat4 type constructor

- swizzle_array - array with swizzle capacity
- tracked_array - modification aware array that can be tracked

- scalar(size,ctype) - array of scalars (tracked)
- vec2(size,ctype) - array of vectors with two components (swizzle + tracked)
- vec3(size,ctype) - array of vectors with three components (swizzle + tracked)
- vec4(size,ctype) - array of vectors with three components (swizzle + tracked)

- mat2(size,ctype) - array of 2x2 matrices (swizzle + tracked)
- mat3(size,ctype) - array of 3x3 matrices (swizzle + tracked)
- mat4(size,ctype) - array of 4x4 matrices (swizzle + tracked)
"""
import numpy as np

ctypes  = [np.int8, np.uint8, np.int16, np.uint16, np.uint32, np.float32]
ctypes += [np.int32, np.int64, np.uint64, np.float64]

def scalar_t(ctype):
    """ Returns a scalar numpy dtype with base type `ctype` """
    
    assert ctype in ctypes
    return np.dtype(ctype)

def vec2_t(ctype):
    """ Returns a vec2 numpy dtype with base type `ctype` """
    
    assert ctype in ctypes
    return np.dtype((ctype, 2))

def vec3_t(ctype):
    """ Returns a vec3 numpy dtype with base type `ctype` """
    
    assert ctype in ctypes
    return np.dtype((ctype, 3))

def vec4_t(ctype):
    """ Returns a vec4 numpy dtype with base type `ctype` """
        
    assert ctype in ctypes
    return np.dtype((ctype, 4))

def mat2_t(ctype):
    """ Returns a mat2 numpy dtype with base type `ctype`. """
        
    assert ctype in ctypes
    return np.dtype((ctype, (2,2)))

def mat3_t(ctype):
    """ Returns a mat3 numpy dtype with base type `ctype`. """
        
    assert ctype in ctypes
    return np.dtype((ctype, (3,3)))

def mat4_t(ctype):
    """ Returns a mat4 numpy dtype with base type `ctype`. """
    
    assert ctype in ctypes
    return np.dtype((ctype, (4,4)))


class tracked_array(np.ndarray):
    """
    A tracked array keeps track of the smallest contiguous block
    of modified memory and can signals a tracker of any change through
    the tracker `set_data` method. A minimal tracker class can thus be
    written as:

    ```
    class Tracker:
        def __init__(self, shape, dtype):
            self._array = np.empty(shape, dtype=dtype)
        def set_data(self, offset, bytes):
            V = self._array.view(np.ubyte).ravel()
            V[offset:offset+len(bytes)] = np.frombuffer(bytes, dtype=np.ubyte)
    ```

    It is the responsability of the user to set the __tracker_class__
    class attribute with the relevant tracker class, prior to the
    creation of any tracked array. If this class is not None, the
    tracker is created at the time of array creation.

    Maintaining a copy of an array as shown in the example above is not very
    interesting. However, you can modify the tracker to mirror a CPU array
    in GPU, by uploading the new data to the GPU in the `set_data` method.
    """
    
    __tracker_class__ = None
    
    def __new__(cls, *args, **kwargs):
        obj = np.ndarray.__new__(cls, *args, **kwargs)
        if cls.__tracker_class__ is not None:
            obj._tracker = cls.__tracker_class__(obj.shape, obj.dtype)
        return obj

    def __array_finalize__(self, obj):

        if not isinstance(obj, tracked_array):
            self.__class__.__init__(self)
        self._extents = 0, self.size*self.itemsize
        self._dirty = self._extents
        self._tracker = getattr(obj, '_tracker', None)
        if self._tracker is None and self.__tracker_class__ is not None:
            self._tracker = self.__tracker_class__(self.shape, self.dtype)

    def clear(self):
        """ Clear dirty region"""

        if isinstance(self.base, tracked_array):
            self.base._dirty = None
        elif self._dirty:
            self._dirty = None

    @property
    def dirty(self):
        """ Dirty region as (start, stop) in bytes """

        if isinstance(self.base, tracked_array):
            return self.base.dirty
        elif self._dirty:
            return self._dirty
        return None

    def _update(self, start, stop):
        """ Update dirty region """
        
        if isinstance(self.base, tracked_array):
            self.base._update(start, stop)
        else:
            if not hasattr(self, "_dirty") or self._dirty is None:
                self._dirty = start, stop
            else:
                start = min(self._dirty[0], start)
                stop = max(self._dirty[1], stop)
                self._dirty = start, stop
                
    def _compute_extents(self, Z):
        """Compute extents (start, stop) in bytes in the base array"""

        if Z.base is not None:
            base = Z.base.__array_interface__['data'][0]
            view = Z.__array_interface__['data'][0]
            offset = view - base
            shape = np.array(Z.shape) - 1
            strides = Z.strides[-len(shape):]
            size = (shape*strides).sum() + Z.itemsize
            return offset, offset+size
        return 0, Z.size*Z.itemsize

    def __getitem__(self, key):
        Z = np.ndarray.__getitem__(self, key)
        if not hasattr(Z, 'shape') or Z.shape == ():
            return Z        
        Z._extents = self._compute_extents(Z)
        return Z

    def __setitem__(self, key, value):
        Z = np.ndarray.__getitem__(self, key)
        
        if Z.shape == ():
            # This test for the case of [...,index] notation. Since we
            # know the result is a scalar, we can safely remove the
            # ellipsis component (that should be the first item).
            if (isinstance(key, tuple)):
                key = tuple([k for k in key if k is not Ellipsis])
            key = tuple(np.mod(np.array(key), self.shape))
            offset = np.ravel_multi_index(key, self.shape, mode='wrap')*self.itemsize
            self._update(offset, offset+self.itemsize)
                    
        # Test for fancy indexing
        elif (Z.base is not self and (isinstance(key, list) or
               (hasattr(key, '__iter__') and
                any(isinstance(k, (list,np.ndarray)) for k in key)))):
            raise NotImplementedError("Fancy indexing not supported")
        else:
            Z._extents = self._compute_extents(Z)            
            self._update(Z._extents[0], Z._extents[1])
        np.ndarray.__setitem__(self, key, value)

        if self._tracker:
            data = self.view(np.ubyte).ravel()
            start, stop = self._dirty
            self._tracker.set_data(start, data[start:stop].tobytes())
            self.clear()

    def __getslice__(self, start, stop):
        return self.__getitem__(slice(start, stop))

    def __setslice__(self, start, stop,  value):
        self.__setitem__(slice(int(start), int(stop)), value)

    def __iadd__(self, other):
        self._update(self._extents[0], self._extents[1])
        return np.ndarray.__iadd__(self, other)

    def __isub__(self, other):
        self._update(self._extents[0], self._extents[1])
        return np.ndarray.__isub__(self, other)

    def __imul__(self, other):
        self._update(self._extents[0], self._extents[1])
        return np.ndarray.__imul__(self, other)

    def __idiv__(self, other):
        self._update(self._extents[0], self._extents[1])
        return np.ndarray.__idiv__(self, other)


class swizzle_array(tracked_array):
    """A swizzle array allows to access the last dimension of an
    array using a virtual attribute whose name is specified at the
    class level. Typical usage is:

    ```
    class vec4(swizzle_array):
        swizzle = "xyzw", "rgba"

    v = vec4()
    v.xyzw = 1,2,3,4 # equivalent to v[[0,1,2,3]] = 1,2,3,4
    v.wzyx = 1,2,3,4 # equivalent to v[[3,2,1,0]] = 1,2,3,4
    ```
    """
    
    swizzle = None

    def __getattr__(self, key):
        for swizzle in self.swizzle:
            if set(key).issubset(set(swizzle)):
                return self[..., [swizzle.index(c) for c in key]]
        return super().__getattribute__(key)

    def __setattr__(self, key, value):
        for swizzle in self.swizzle:
            if set(key).issubset(set(swizzle)):
                value = np.asarray(value)
                shape = value.shape
                indices = [swizzle.index(c) for c in key]
                if not len(shape):
                    for index in indices:
                        self[..., index] = value
                    break
                elif shape[-1] == 1:
                    for index in indices:
                        self[..., index] = np.squeeze(value)
                    break
                elif shape[-1] == len(key):
                    for tgt_index, src_index in enumerate(indices):
                        if self[...,src_index].size == value[...,tgt_index].size:
                            self[...,src_index] = value[...,tgt_index].reshape(self[...,src_index].shape)
                        else:
                            
                            self[...,src_index] = value[...,tgt_index]
                    break
                else:
                    raise IndexError
        else:
            super().__setattr__(key, value)

    
class scalar(tracked_array):
    """Array of scalars (tracked)"""
    
    def __new__(subtype, shape=1, ctype=np.float32, buffer=None,
                offset=0, strides=None, order=None, info=None):
        return super().__new__(subtype, shape, scalar_t(ctype),
                               buffer, offset, strides, order)

class vec2(swizzle_array):
    """Array of vectors with two components (swizzle + tracked).
    Components can be accessed with xy or ra."""
    
    swizzle = "xy", "ra"
    
    def __new__(subtype, shape=1, ctype=np.float32, buffer=None,
                offset=0, strides=None, order=None, info=None):
        return super().__new__(subtype, shape, vec2_t(ctype),
                               buffer, offset, strides, order)

class vec3(swizzle_array):
    """Array of vectors with three components (swizzle + tracked).
    Components can be accessed with xyz or rgb."""
        
    swizzle = "xyz", "rgb"
    
    def __new__(subtype, shape=1, ctype=np.float32, buffer=None,
                offset=0, strides=None, order=None, info=None):
        return super().__new__(subtype, shape, vec3_t(ctype),
                              buffer, offset, strides, order)

class vec4(swizzle_array):
    """Array of vectors with four components (swizzle + tracked).
    Components can be accessed with xyzw or rgba."""
    
    swizzle = "xyzw", "rgba"
    
    def __new__(subtype, shape=1, ctype=np.float32, buffer=None,
                offset=0, strides=None, order=None, info=None):
        return super().__new__(subtype, shape, vec4_t(ctype),
                               buffer, offset, strides, order)

class mat2(swizzle_array):
    """Array of 2x2 matrices (swizzle + tracked). Components can be
    accessed with xy or ra."""

    swizzle = "xy", "ra"
    
    def __new__(subtype, shape=1, ctype=np.float32, buffer=None,
                offset=0, strides=None, order=None, info=None):
        return super().__new__(subtype, shape, mat2_t(ctype),
                               buffer, offset, strides, order)

class mat3(swizzle_array):
    """Array of 3x3 matrices (swizzle + tracked). Components can be
    accessed with xyz or rgb."""

    swizzle = "xyz", "rgb"
    
    def __new__(subtype, shape=1, ctype=np.float32, buffer=None,
                offset=0, strides=None, order=None, info=None):
        return super().__new__(subtype, shape, mat3_t(ctype),
                               buffer, offset, strides, order)

class mat4(swizzle_array):
    """Array of 4x4 matrices (swizzle + tracked). Components can be
    accessed with xyzw or rgba."""

    swizzle = "xyzw", "rgba"
    
    def __new__(subtype, shape=1, ctype=np.float32, buffer=None,
                offset=0, strides=None, order=None, info=None):
        return super().__new__(subtype, shape, mat4_t(ctype),
                               buffer, offset, strides, order)
