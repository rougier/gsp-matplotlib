# Package: Graphic Server Protocol / Matplotlib
# Authors: Nicolas P .Rougier <nicolas.rougier@inria.fr>
# License: BSD 3 clause
import numpy as np


def sRGB_to_RGB(color):


    color = np.asarray(color, dtype=float).reshape(-1, 3)
    R, G, B = color[..., 0], color[..., 1], color[..., 2]
    R = np.where(R > 0.04045, np.power((R + 0.055) / 1.055, 2.4), R / 12.92)
    G = np.where(G > 0.04045, np.power((G + 0.055) / 1.055, 2.4), G / 12.92)
    B = np.where(B > 0.04045, np.power((B + 0.055) / 1.055, 2.4), B / 12.92)
    return np.c_[R, G, B]

def RGB_to_sRGB(color):
    """ OKLAb model """

    color = np.asarray(color, dtype=float).reshape(-1, 3)
    R, G, B = color[..., 0], color[..., 1], color[..., 2]
    R = np.where(R > 0.0031308, 1.055 * np.power(R, 1 / 2.4) - 0.055, R * 12.92)
    G = np.where(G > 0.0031308, 1.055 * np.power(G, 1 / 2.4) - 0.055, G * 12.92)
    B = np.where(B > 0.0031308, 1.055 * np.power(B, 1 / 2.4) - 0.055, B * 12.92)
    return np.c_[R, G, B]

def sRGBA_to_RGBA(color):
    """ OKLAb model """

    color = np.asarray(color, dtype=float).reshape(-1, 4)
    R, G, B, A = color[..., 0], color[..., 1], color[..., 2], color[..., 3]
    R = np.where(R > 0.04045, np.power((R + 0.055) / 1.055, 2.4), R / 12.92)
    G = np.where(G > 0.04045, np.power((G + 0.055) / 1.055, 2.4), G / 12.92)
    B = np.where(B > 0.04045, np.power((B + 0.055) / 1.055, 2.4), B / 12.92)
    return np.c_[R, G, B, A]


def RGBA_to_sRGBA(color):
    """ OKLAb model """

    color = np.asarray(color, dtype=float).reshape(-1, 4)
    R, G, B, A = color[..., 0], color[..., 1], color[..., 2], color[..., 3]
    R = np.where(R > 0.0031308, 1.055 * np.power(R, 1 / 2.4) - 0.055, R * 12.92)
    G = np.where(G > 0.0031308, 1.055 * np.power(G, 1 / 2.4) - 0.055, G * 12.92)
    B = np.where(B > 0.0031308, 1.055 * np.power(B, 1 / 2.4) - 0.055, B * 12.92)
    return np.c_[R, G, B, A]

# def sRGBA_to_RGBA(color):
#     color = np.asarray(color, dtype=float).reshape(-1, 4)
#     color[...,:3] = np.power(color[:,:3],2.2)
#     return color

# def RGBA_to_sRGBA(color):
#     color = np.asarray(color, dtype=float).reshape(-1, 4)
#     color[...,:3] = np.power(color[:,:3],1/2.2)
#     return color
