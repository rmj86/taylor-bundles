# -*- coding: utf-8 -*-

from numpy import pi, cos, sqrt, array, newaxis, full, exp, log
from matplotlib.colors import colorConverter
from matplotlib.cm import get_cmap
from types import FunctionType

tau = 2*pi

def fromConstant(color):
    """ Takes any valid color argument, and returns a corresponding
        color function. Constants are tuirned into constant
        functions. Functions are returned unchanged. """
    if type(color) == FunctionType:
        return color
    else:
        c_arr = colorConverter.to_rgba_array(color)
        def const_color(t):
            return full(t.shape+(4,), c_arr)
        return const_color

# Helper function for mix2. Guarantees that the norm parameter doesn't
#exceed the interval [0,1]; if it did, the rgba color values out may
# exceed [0,1], which makes matplotlib throw an error.
def _bounded(t):
    """ Takes an ndarray `t` as input, and returns it with
        values bounded to the interval [0,1]. Values in t<0
        are set to 0, and values in t>1 are set to 1.
        Mutates ``t"""
    t[t<0] = 0
    t[t>1] = 1
    return t

def colormap(cmap_name, norm):
    cmap = get_cmap(cmap_name)
    def colorfunc(t):
        return cmap(norm(t))
    return colorfunc

def mix2(color1, color2, norm, linear=True):
    """ retuns a function mix(t) which takes an array of curve
        parameters and returns an array of rgba-tuples. norm is
        a function from the curve parameter t to values in the
        range [0,1]. Where the norm is closer to 0, shows more
        of color1. Where closer to 1, more of color2.
        When linear==True, mix in a linear color space."""
    cfunc1 = fromConstant(color1)
    cfunc2 = fromConstant(color2)
    def mix(t):
        m = _bounded(norm(t))[:,newaxis]
        c1 = cfunc1(t)
        c2 = cfunc2(t)
        if linear:
            return sqrt((1-m)*(c1*c1) + m*(c2*c2))
        else:
            return (1-m)*c1 + m*c2
    return mix

## Normalization functions 

def normalize(u, v):
    """returns a function f that linearly transforms
        the interval [u,v] to [0,1]. """
    def _norm(t):
        return (t-u)/float(v-u)
    return _norm

def smoothstep(u, v):
    """ A smooth step from 0 to 1 in the domain [u,v]. When
        t<u, is constant 0. When v<t, is constant 1."""
    norm = normalize(u, v)
    def _smoothstep_norm(t):
        ts = norm(t)  # scale t so that [u,v] becomes [0,1]
        m = ts*ts*(3-2*ts)
        m[ts<0] = 0
        m[ts>1] = 1
        return m
    return _smoothstep_norm

def cosine(p1, p2):
    """ A cosine curve oscillating between 0 and 1. It is 0
        where t=p1, 1 where t=p2, and has period 2*(p2-p1). """
    norm = normalize(p1, p2)
    def _cosine_norm(t):
        ts = pi * norm(t)  # scale t so [p1,p2] becomes [0,pi]
        m = 0.5 * (1 - cos(ts))
        return m
    return _cosine_norm

def gaussian(c, w):
    """ A gaussian curve with it's peak at c and width w.
        Width refers to it's "full width at half maximum"."""
    s = 2*sqrt(log(2)) / w  # scaling factor for t
    def _gaussian_norm(t):
        ts = (t-c)*s  # t scaled so that [c-w, c+w] is FWHM range
        m = exp(-ts*ts)
        return m
    return _gaussian_norm
