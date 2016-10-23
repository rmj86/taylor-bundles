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

def mix2(color1, color2, map, linear=True):
    """ retuns a function mix(t) which takes an array of curve
        parameters and returns an array of rgba-tuples. map is
        a function from the curve parameter t to values in the
        range [0,1]. Where the map is 0, shows color1, where
        the map is 1, shows color2.
        When linear==True, mix in a linear color space."""
    cfunc1 = fromConstant(color1)
    cfunc2 = fromConstant(color2)
    def mix(t):
        m = map(t)[:,newaxis]
        c1 = cfunc1(t)
        c2 = cfunc2(t)
        if linear:
            return sqrt((1-m)*(c1*c1) + m*(c2*c2))
        else:
            return (1-m)*c1 + m*c2
    return mix

def smoothstep(u, v):
    """ A smooth step from 0 to 1 in the domain [u,v]. When
        t<u, is constant 0. When v<t, is constant 1."""
    def step(t):
        ts = (t-u)/(v-u)  # scale t so that [u,v] becomes [0,1]
        m = ts*ts*(3-2*ts)
        m[ts<0] = 0
        m[ts>1] = 1
        return m
    return step

def cosine(p1, p2):
    """ A cosine curve oscillating between 0 and 1. It is 0
        where t=p1, 1 where t=p2, and has period 2*(p2-p1). """
    period = 2*(p2-p1)
    const = tau/period # ???
    def oscillator(t):
        ts = pi/(p2-p1) * (p1-t) # scale t so [p1,p2] becomes [0,pi]
        m = 0.5 * (1 - cos(ts))
        return m
    return oscillator

def gaussian(c, w):
    """ A gaussian curve with it's peak at c and width w.
        Width refers to it's "full width at half maximum"."""
    s = 2*sqrt(log(2)) / w  # scaling factor for t
    def bellcurve(t):
        ts = (t-c)*s  # t scaled so that [c-w, c+w] is FWHM range
        m = exp(-ts*ts)
        return m
    return bellcurve
