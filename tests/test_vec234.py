# -----------------------------------------------------------------------------
# Graphic Server Protocol (GSP)
# Copyright 2023 Vispy Development Team - BSD 2 Clauses licence
# -----------------------------------------------------------------------------
import pytest
import numpy as np
from gsp.glm import scalar, vec2, vec3, vec4
from gsp.glm import scalar_t, vec2_t, vec3_t, vec4_t

def test_dtypes():
    assert(vec2_t(np.float32).base == np.float32)
    assert(vec2_t(np.float32).shape == (2,))
    assert(vec3_t(np.float32).base == np.float32)
    assert(vec3_t(np.float32).shape == (3,))
    assert(vec4_t(np.float32).base == np.float32)
    assert(vec4_t(np.float32).shape == (4,))

def test_default_type():
    assert(scalar().dtype == np.float32)
    assert(vec2().dtype == np.float32)
    assert(vec3().dtype == np.float32)
    assert(vec4().dtype == np.float32)

def test_default_shape():
    assert(scalar().shape == (1,))
    assert(vec2().shape == (1,2))
    assert(vec3().shape == (1,3))
    assert(vec4().shape == (1,4))

def test_ctype():
    assert(scalar(1, np.ubyte).dtype == np.ubyte)
    assert(vec2(1, np.ubyte).dtype == np.ubyte)
    assert(vec3(1, np.ubyte).dtype == np.ubyte)
    assert(vec4(1, np.ubyte).dtype == np.ubyte)

def test_shape():
    assert(scalar(10).shape == (10,))
    assert(vec2(10).shape == (10,2))
    assert(vec3(10).shape == (10,3))
    assert(vec4(10).shape == (10,4))

    assert(scalar((3,3)).shape == (3,3))
    assert(vec2((3,3)).shape == (3,3,2))
    assert(vec3((3,3)).shape == (3,3,3))
    assert(vec4((3,3)).shape == (3,3,4))

def test_view():
    Z = np.zeros(2*10, np.float32).view(vec2)
    assert(isinstance(Z,vec2))

    Z = np.zeros(3*10, np.float32).view(vec3)
    assert(isinstance(Z,vec3))

    Z = np.zeros(4*10, np.float32).view(vec4)
    assert(isinstance(Z,vec4))

