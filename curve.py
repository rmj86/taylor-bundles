# -*- coding: utf-8 -*-

import numpy
from numpy import sin, cos
from numpy.polynomial import Polynomial
from math import factorial

def numDiff(f, a, n=1, h=0.02):
    """ Numeric nth derivative of function f at point x=a, using symmetric
        finite difference method with point sampling distance h. """
    i = numpy.linspace(-n, n, n+1)
    x = a + (h/2.0)*i
    y = f(x)
    difference = numpy.diff(y, n)
    derivative = difference / (h**n)
    return derivative[0]

def taylorPoly(f, a, n=1, df=None):
    """ Degree n Taylor polynomial of f(x) around the point x=a. """
    if df is None:
        df = lambda a, n: numDiff(f, a, n)
    p = Polynomial([0])
    
    for i in range(n+1):
        q = Polynomial([-a,1])
        q.maxpower = i
        p = p + q**i * df(a,i) / factorial(i)
    return p


class Curve:
    """ Parametric 2D curve. """
    def __init__(self, x, y, dx=None, dy=None):
        self.x = x
        self.y = y
        if dx is None:
            def dx(a, n): return numDiff(self.x, a, n)
        if dy is None:
            def dy(a, n): return numDiff(self.y, a, n)
        self.dx = dx
        self.dy = dy
    def taylorCurve(self, a, n=1):
        """ Taylor curve about the point t=a. """
        px = taylorPoly(self.x, a, n, df=self.dx)
        py = taylorPoly(self.y, a, n, df=self.dy)
        return Curve(px, py)
    def __call__(self, t):
        ps = numpy.ndarray(t.shape+(2,))
        ps[:,0] = self.x(t)
        ps[:,1] = self.y(t)
        return ps
    def __add__(self, other):
        def sum_x(t): return self.x(t) + other.x(t)
        def sum_y(t): return self.y(t) + other.y(t)
        def sum_dx(a, n): return self.dx(a, n) + other.dx(a, n)
        def sum_dy(a, n): return self.dy(a, n) + other.dy(a, n)
        return Curve(sum_x, sum_y, sum_dx, sum_dy)

def fromFunction(f):
    """takes a function  f  and returns a Curve object representing
       the parametric curve  <t, f(t)>"""
    x = lambda t: t
    # y = lambda t: f(t)
    # c = Curve(x, y)
    c = Curve(x, f)
    return c

sinprime_memo = [sin, cos, lambda x: -sin(x), lambda x: -cos(x)]
def sinprime(n):
    """ nth derivative os sin(x). """
    return sinprime_memo[n%4]

cosprime_memo = [cos, lambda x: -sin(x), lambda x: -cos(x), sin]
def cosprime(n):
    """ nth derivative of cos(x). """
    return cosprime_memo[n%4]

# class Point(Curve):
    # def __init__(self, x, y):
        # def px(t):
            # t_ = t.copy()
            # t_ = x
            # return t
        # def py(t): return t
        # dx = lambda t: 0
        # dy = lambda t: 0

# class Line

# class Circle
    # def __init__(self, r, omega, offset

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
            cp = cosprime(d) # d:th derivative of cos
            return cp(a) + r*(n+1)**d*cp((n+1)*a + o)
        def y_derivative(a, d=1):
            sp = sinprime(d)  # d:th derivative of sin
            return sp(a) + r*(n+1)**d*sp((n+1)*a + o)
        Curve.__init__(self, x, y)
        self.x.derivative = x_derivative
        self.y.derivative = y_derivative
# TODO derivative
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
            return A * a**d * sinprime(d)(a*t + delta)
        def y_derivative(t, d=1):
            return B * b**d * sinprime(d)(b*t)
        Curve.__init__(self, x, y)
        self.x.derivative = x_derivative
        self.y.derivative = y_derivative

