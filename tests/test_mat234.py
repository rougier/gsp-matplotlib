# -----------------------------------------------------------------------------
# Graphic Server Protocol (GSP)
# Copyright 2023 Vispy Development Team - BSD 2 Clauses licence
# -----------------------------------------------------------------------------
import pytest
import numpy as np
from gsp.glm import ndarray


def test_dtypes():
    assert(ndarray.mat2_t(np.float32).base == np.float32)
    assert(ndarray.mat2_t(np.float32).shape == (2,2))
    assert(ndarray.mat3_t(np.float32).base == np.float32)
    assert(ndarray.mat3_t(np.float32).shape == (3,3))
    assert(ndarray.mat4_t(np.float32).base == np.float32)
    assert(ndarray.mat4_t(np.float32).shape == (4,4))


def test_default_type():
    assert(ndarray.mat2().dtype == np.float32)
    assert(ndarray.mat3().dtype == np.float32)
    assert(ndarray.mat4().dtype == np.float32)

def test_default_shape():
    assert(ndarray.mat2().shape == (2,2))
    assert(ndarray.mat3().shape == (3,3))
    assert(ndarray.mat4().shape == (4,4))

def test_ctype():
    assert(ndarray.mat2(1, np.ubyte).dtype == np.ubyte)
    assert(ndarray.mat3(1, np.ubyte).dtype == np.ubyte)
    assert(ndarray.mat4(1, np.ubyte).dtype == np.ubyte)

def test_shape():
    assert(ndarray.mat2(10).shape == (10,2,2))
    assert(ndarray.mat3(10).shape == (10,3,3))
    assert(ndarray.mat4(10).shape == (10,4,4))

    assert(ndarray.mat2((3,3)).shape == (3,3,2,2))
    assert(ndarray.mat3((3,3)).shape == (3,3,3,3))
    assert(ndarray.mat4((3,3)).shape == (3,3,4,4))

def test_view():
    Z = np.zeros(2*10, np.float32).view(ndarray.mat2)
    assert(isinstance(Z,ndarray.mat2))

    Z = np.zeros(3*10, np.float32).view(ndarray.mat3)
    assert(isinstance(Z,ndarray.mat3))

    Z = np.zeros(4*10, np.float32).view(ndarray.mat4)
    assert(isinstance(Z,ndarray.mat4))
