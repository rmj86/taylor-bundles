# -*- coding: utf-8 -*-
"""
Created on Wed Feb 17 22:45:14 2016

@author: hannes
"""

from numpy import pi, cos, sqrt, array, newaxis, full, exp, power
from matplotlib.colors import colorConverter
from types import FunctionType

tau = 2*pi

def fromConstant(color):
    if type(color) == FunctionType: # assume its valid and return unchanged
        return color
    else:  # it is a constant
        c_arr = colorConverter.to_rgba_array(color)
        def const_color(t):
            return full(t.shape+(4,), c_arr)
        return const_color
    
def cosine2(color1, color2, u, v, linear=True):
    """ returns a function mix(t) which mixes colors c1 and c2. c1 and c2
        are  any valid matplotlib color. E.g. a color char ('r'), a html
        color name ("red"), a html hex color ("#FF0000") or a 3- or 4-tuple.
        u is the peak of c1, and v is the peak of c2. To mix in a liear
        color space, use linear=True.
        The returned mix function takes a numpy array with shape (n,) and
        returns a numpy array with shape (n,4) - rgba."""
    period = 2*(v-u)
    const = tau/period
    cfunc1 = fromConstant(color1)
    cfunc2 = fromConstant(color2)
    def mix(t):
        m = 0.5 * (1 + cos((t-u) * (tau/period)))
        m = m[:, newaxis]
        c1 = cfunc1(t)
        c2 = cfunc2(t)
        if linear:
            return sqrt(m*(c1**2) + (1-m)*(c2**2))
        else:
            return m*c1 + (1-m)*c2
    return mix

def gaussian(color1, color2, mu, sigma, linear=True):
    """ Mix color1 and color2 according to a gaussian fuinction.
        There is a single peak of color1 on top of color2, with
        center mu and width sigma. """
    cfunc1 = fromConstant(color1)
    cfunc2 = fromConstant(color2)
    def mix(t):
        m = exp(-power(t - mu, 2.) / (2 * power(sigma, 2.)))
        m = m[:, newaxis]
        c1 = cfunc1(t)
        c2 = cfunc2(t)
        if linear:
            return sqrt(m*(c1**2) + (1-m)*(c2**2))
        else:
            return m*c1 + (1-m)*c2
    return mix
