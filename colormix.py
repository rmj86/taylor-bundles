# -*- coding: utf-8 -*-

from numpy import pi, cos, sqrt, array, newaxis, full, exp, log
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
    
def cosine2(color1, color2, peak1, peak2, linear=True):
    """ returns a function mix(t) which mixes colors c1 and c2. c1 and c2
        are  any valid matplotlib color. E.g. a color char ('r'), a html
        color name ("red"), a html hex color ("#FF0000") or a 3- or 4-tuple.
        peak1 is the peak of color1, and peak2 is the peak of color2. Colors are mixed in a linear colorspace by default. Use "normal" colorspace
        by setting linear=False.
        The returned mix function takes a numpy array with shape (n,) and
        returns a numpy array with shape (n,4) - rgba."""
    period = 2*(peak2-peak1)
    const = tau/period
    cfunc1 = fromConstant(color1)
    cfunc2 = fromConstant(color2)
    def mix(t):
        m = 0.5 * (1 + cos((t-peak1) * (tau/period)))
        m = m[:, newaxis]
        c1 = cfunc1(t)
        c2 = cfunc2(t)
        if linear:
            return sqrt(m*(c1**2) + (1-m)*(c2**2))
        else:
            return m*c1 + (1-m)*c2
    return mix

def gaussian(color1, color2, center, width, linear=True):
    """ Mix color1 and color2 according to a gaussian fuinction.
        There is a single peak of color1 on top of color2, with the
        given center and width. width is 'full width at half macimum.'"""
    cfunc1 = fromConstant(color1)
    cfunc2 = fromConstant(color2)
    c = width / (2*sqrt(2*log(2)))
    def mix(t):
        tc = t-center
        m = exp((tc*tc) / (-2*c*c))
        m = m[:, newaxis]
        c1 = cfunc1(t)
        c2 = cfunc2(t)
        if linear:
            return sqrt(m*(c1**2) + (1-m)*(c2**2))
        else:
            return m*c1 + (1-m)*c2
    return mix
