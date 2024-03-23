# -----------------------------------------------------------------------------
# Graphic Server Protocol (GSP)
# Copyright 2023 Vispy Development Team - BSD 2 Clauses licence
# -----------------------------------------------------------------------------
import pytest
import numpy as np
from gsp.glm import ndarray

def test_dtypes():
    assert(ndarray.vec2_t(np.float32).base == np.float32)
    assert(ndarray.vec2_t(np.float32).shape == (2,))
    assert(ndarray.vec3_t(np.float32).base == np.float32)
    assert(ndarray.vec3_t(np.float32).shape == (3,))
    assert(ndarray.vec4_t(np.float32).base == np.float32)
    assert(ndarray.vec4_t(np.float32).shape == (4,))

def test_default_type():
    assert(ndarray.scalar().dtype == np.float32)
    assert(ndarray.vec2().dtype == np.float32)
    assert(ndarray.vec3().dtype == np.float32)
    assert(ndarray.vec4().dtype == np.float32)

def test_default_shape():
    assert(ndarray.scalar().shape == ())
    assert(ndarray.vec2().shape == (2,))
    assert(ndarray.vec3().shape == (3,))
    assert(ndarray.vec4().shape == (4,))

def test_ctype():
    assert(ndarray.scalar(1, np.ubyte).dtype == np.ubyte)
    assert(ndarray.vec2(1, np.ubyte).dtype == np.ubyte)
    assert(ndarray.vec3(1, np.ubyte).dtype == np.ubyte)
    assert(ndarray.vec4(1, np.ubyte).dtype == np.ubyte)

def test_shape():
    assert(ndarray.scalar(10).shape == (10,))
    assert(ndarray.vec2(10).shape == (10,2))
    assert(ndarray.vec3(10).shape == (10,3))
    assert(ndarray.vec4(10).shape == (10,4))

    assert(ndarray.scalar((3,3)).shape == (3,3))
    assert(ndarray.vec2((3,3)).shape == (3,3,2))
    assert(ndarray.vec3((3,3)).shape == (3,3,3))
    assert(ndarray.vec4((3,3)).shape == (3,3,4))

def test_view():
    Z = np.zeros(2*10, np.float32).view(ndarray.vec2)
    assert(isinstance(Z,ndarray.vec2))

    Z = np.zeros(3*10, np.float32).view(ndarray.vec3)
    assert(isinstance(Z,ndarray.vec3))

    Z = np.zeros(4*10, np.float32).view(ndarray.vec4)
    assert(isinstance(Z,ndarray.vec4))

