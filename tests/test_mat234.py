# -----------------------------------------------------------------------------
# Graphic Server Protocol (GSP)
# Copyright 2023 Vispy Development Team - BSD 2 Clauses licence
# -----------------------------------------------------------------------------
import pytest
import numpy as np
from gsp.glm import scalar, mat2, mat3, mat4
from gsp.glm import scalar_t, mat2_t, mat3_t, mat4_t

def test_dtypes():
    assert(mat2_t(np.float32).base == np.float32)
    assert(mat2_t(np.float32).shape == (2,2))
    assert(mat3_t(np.float32).base == np.float32)
    assert(mat3_t(np.float32).shape == (3,3))
    assert(mat4_t(np.float32).base == np.float32)
    assert(mat4_t(np.float32).shape == (4,4))


def test_default_type():
    assert(scalar().dtype == np.float32)
    assert(mat2().dtype == np.float32)
    assert(mat3().dtype == np.float32)
    assert(mat4().dtype == np.float32)

def test_default_shape():
    assert(scalar().shape == (1,))
    assert(mat2().shape == (1,2,2))
    assert(mat3().shape == (1,3,3))
    assert(mat4().shape == (1,4,4))

def test_ctype():
    assert(scalar(1, np.ubyte).dtype == np.ubyte)
    assert(mat2(1, np.ubyte).dtype == np.ubyte)
    assert(mat3(1, np.ubyte).dtype == np.ubyte)
    assert(mat4(1, np.ubyte).dtype == np.ubyte)

def test_shape():
    assert(scalar(10).shape == (10,))
    assert(mat2(10).shape == (10,2,2))
    assert(mat3(10).shape == (10,3,3))
    assert(mat4(10).shape == (10,4,4))

    assert(scalar((3,3)).shape == (3,3))
    assert(mat2((3,3)).shape == (3,3,2,2))
    assert(mat3((3,3)).shape == (3,3,3,3))
    assert(mat4((3,3)).shape == (3,3,4,4))

def test_view():
    Z = np.zeros(2*10, np.float32).view(mat2)
    assert(isinstance(Z,mat2))

    Z = np.zeros(3*10, np.float32).view(mat3)
    assert(isinstance(Z,mat3))

    Z = np.zeros(4*10, np.float32).view(mat4)
    assert(isinstance(Z,mat4))
