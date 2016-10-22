# -*- coding: utf-8 -*-
"""
Created on Mon Feb 15 17:43:23 2016

@author: hannes
"""

import numpy
from numpy import sin, cos
from numpy.polynomial import Polynomial
from math import factorial

def derivative(f, a, d=1):
    """ Derivative of function f at point x=a to degree d. Can give exact
        derivative if f.derivative is defined. Otherwise it defaults to
        numerical derivative. """
    if "derivative" in dir(f):
        return f.derivative(a, d)
    else:
        return derivative_numerical(f, a, d)

def derivative_numerical(f, a, d=1, h=0.02):
    """ Numeric derivative of function f at point x=a.
        Derivative of degree d, with point sampling distance h. """
    i = numpy.linspace(-d, d, d+1)
    x = a + (h/2.0)*i
    y = f(x)
    difference = numpy.diff(y, d)
    derivative = difference / (h**d)
    return derivative[0]

def taylorExpansion(f, a, d=1):
    """ Taylor polynomial expansion of f(x) around the point x=a to degree d. """
    p = Polynomial([0])
    for i in range(d+1):
        q = Polynomial([-a,1])
        q.maxpower = i
        p = p + q**i * derivative(f,a,i) / factorial(i)
    return p

class Curve:
    """Parametric 2D curve."""
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def taylorCurve(self, a, d=1):
        """Approximation of self via Taylor expansion around the point t=a. """
        px = taylorExpansion(self.x, a, d)
        py = taylorExpansion(self.y, a, d)
        return Curve(px, py)

def fromFunction(f):
    """takes a function  f  and returns a Curve object representing
       the parametric curve  <t, f(t)>"""
    x = lambda t: t
    y = lambda t: f(t)
    c = Curve(x, y)
    return c

# the derivatives of sin; cyclic
sinprime = [sin, cos, lambda x: -sin(x), lambda x: -cos(x)]
# The derivatives of cos; cyclic
cosprime = sinprime[1:] + [sinprime[0]]

class Trochoid(Curve):
    def __init__(self, n, r, o=0.0, **kwargs):
        """ n: Number f loops. Positive n makes epitrochoid,
                               negative n makes hypotrochoid.
            r: radius of the rolling part. (fixed part has radius 1)
            o: rotational offset of rolling part. """
        def x(t):
            return cos(t) + r * cos((n+1)*t + o)
        def y(t):
            return sin(t) + r * sin((n+1)*t + o)
        def x_derivative(a, d=1):
            cp = cosprime[d%4] # d:th derivative of cos
            return cp(a) + r*(n+1)**d*cp((n+1)*a + o)
        def y_derivative(a, d=1):
            sp = sinprime[d%4]  # d:th derivative of sin
            return sp(a) + r*(n+1)**d*sp((n+1)*a + o)
        Curve.__init__(self, x, y)
        self.x.derivative = x_derivative
        self.y.derivative = y_derivative

class Lissajous(Curve):
    def __init__(self, a, b, A, B, delta):
        """ x = A * sin(a + delta)
            y = B * sin(b)
            https://en.wikipedia.org/wiki/Lissajous_curve """
        def x(t):
            return A * sin(a*t + delta)
        def y(t):
            return B * sin(b*t)
        def x_derivative(t, d=1):
            return A * a**d * sinprime[d%4](a*t + delta)
        def y_derivative(t, d=1):
            return B * b**d * sinprime[d%4](b*t)
        Curve.__init__(self, x, y)
        self.x.derivative = x_derivative
        self.y.derivative = y_derivative
