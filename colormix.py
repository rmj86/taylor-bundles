# -*- coding: utf-8 -*-
"""
Created on Wed Feb 17 22:45:14 2016

@author: hannes
"""

from numpy import pi, cos, sqrt, array

tau = 2*pi

def constant(color):
    def mix(t):
        return color
    return mix

def cosine2(color1, color2, u, v, linear=False):
    """ returns a function mix(t) which mixes colors c1 and c2. c1 and c2 are 
        RGB 3-tuplets (The length is not checked). u is the peak of c1, and v 
        is the peak of c2. To mix in a liear color space, use linear=True."""
    period = 2*(v-u)
    c1, c2 = array(color1), array(color2)
    if linear:
        def mix(t):
            m = 0.5 * (1 + cos((t-u) * tau/period))
            return sqrt(m*c1**2 + (1-m)*c2**2)
    else:
        def mix(t):
            m = 0.5 * (1 + cos((t-u) * tau/period))
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