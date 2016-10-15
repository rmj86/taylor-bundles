# -*- coding: utf-8 -*-
"""
Created on Wed Feb 17 22:45:14 2016

@author: hannes
"""

from numpy import pi, cos, sqrt, array, newaxis
from matplotlib.colors import colorConverter

tau = 2*pi

def constant(color):
    def mix(t):
        return color
    return mix

def cosine2(color1, color2, u, v, linear=False):
    """ returns a function mix(t) which mixes colors c1 and c2. c1 and c2
        are  any valid matplotlib color. E.g. a color char ('r'), a html
        color name ("red"), a html hex color ("#FF0000") or a 3- or 4-tuple.
        u is the peak of c1, and v is the peak of c2. To mix in a liear
        color space, use linear=True.
        The returned mix function takes a numpy array with shape (n,) and
        returns a numpy array with shape (n,4) - rgba."""
    period = 2*(v-u)
    const = tau/period
    c1 = colorConverter.to_rgba_array(color1)
    c2 = colorConverter.to_rgba_array(color2)
    if linear:
        def mix(t):
            m = 0.5 * (1 + cos((t-u) * const))
            m = m[:,newaxis]
            return sqrt(m*c1**2 + (1-m)*c2**2)
    else:
        def mix(t):
            # TODO: should take numpy array argument
            m = 0.5 * (1 + cos((t-u) * const))
            m = m[:,newaxis]
            return m*c1 + (1-m)*c2
            
            
            
    return mix
    
def main():
    import numpy
    cm = cosine2((1,0,0),(0,0,1),0,1)
    t = numpy.linspace(0,1,9)
    c = cm(t[:,numpy.newaxis])
    print cm(0)
    print cm(0).shape
    print 
    print c
    print c.shape

if __name__ == "__main__":
    main()