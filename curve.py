# -*- coding: utf-8 -*-

import numpy
from numpy import sin, cos, zeros, ones, newaxis
from numpy.polynomial import Polynomial
from math import factorial


################################################################################
## Taylor Polynomials

def pascal(n, memo={0: numpy.array([[1]])}):
    """ rows of binomial coefficients, (n+1) square array, with the
        rows on the rising diagonals. """
    if n in memo:
        return memo[n]
    prev = pascal(n-1)
    this = zeros((n+1,n+1))
    this[:-1, :-1] = prev
    prev_diag = numpy.diagonal(prev[:,::-1])
    this_diag = ones((n+1))
    this_diag[1:-1] = prev_diag[:-1] + prev_diag[1:]
    numpy.fill_diagonal(this[:,::-1], this_diag)
    memo[n] = this
    return this

def taylorPoly(f, a, n=1, df=None):
    """ Degree n Taylor polynomial of f(x) around the point x=a. """
    if df is None:
        df = lambda a, n: numDiff(f, a, n)
    fprime = zeros(((n+1),(n+1)))
    for i in range(n+1):
        value = df(a, i) / factorial(i)
        for j in range(i+1):
            x, y = i-j, j
            fprime[x,y] = value
    pasc = pascal(n)
    alpha = (-a)**numpy.arange(n+1)
    terms = alpha[newaxis,:] * pasc * fprime
    coeff = numpy.sum(terms, axis=1)
    return Polynomial(coeff)

################################################################################
## Calculus helper functions

def numDiff(f, a, n=1, h=0.02):
    """ Numeric nth derivative of function f at point x=a, using symmetric
        finite difference method with point sampling distance h. """
    i = numpy.linspace(-n, n, n+1)
    x = a + (h/2.0)*i
    y = f(x)
    difference = numpy.diff(y, n)
    derivative = difference / (h**n)
    return derivative[0]

sinprime_memo = [sin, cos, lambda x: -sin(x), lambda x: -cos(x)]
def sinprime(n):
    """ nth derivative of sin(x). """
    return sinprime_memo[n%4]

cosprime_memo = [cos, lambda x: -sin(x), lambda x: -cos(x), sin]
def cosprime(n):
    """ nth derivative of cos(x). """
    return cosprime_memo[n%4]

################################################################################
## Other helper fnctions

def aconst(x, dtype=numpy.float64):
    """ returns an array function, constant in the value `x`. """
    def _constf(t):
        return numpy.full_like(t, x, dtype=dtype)
    return _constf

################################################################################
## Curve base class

class Curve:
    """ Parametric 2D curve. """
    def __init__(self, x, y, dx=None, dy=None):
        self.x = x
        self.y = y
        if dx is None:
            def dx(a, n=1): return numDiff(self.x, a, n)
        if dy is None:
            def dy(a, n=1): return numDiff(self.y, a, n)
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
        def sum_dx(a, n=1): return self.dx(a, n) + other.dx(a, n)
        def sum_dy(a, n=1): return self.dy(a, n) + other.dy(a, n)
        return Curve(sum_x, sum_y, sum_dx, sum_dy)

def fromFunction(f):
    """takes a function  f  and returns a Curve object representing
       the parametric curve  <t, f(t)>"""
    x = lambda t: t
    c = Curve(x, f)
    return c

################################################################################
## Primitive curves

class Point(Curve):
    def __init__(self, x0, y0):
        """ A parametric point, i.e. a parametric curve  <x(t),y(t)>
            such that  x(t) = `x0`, y(t) = `x0`  for all t. """
        fx = aconst(x0)
        fy = aconst(y0)
        def dx(a, n=1):
            if n==0: return x0
            else: return 0
        def dy(a, n=1):
            if n==0: return y0
            else: return 0
        Curve.__init__(self, fx, fy, dx, dy)

class Line(Curve):
    def __init__(self, a, b):
        """ Parametric line through (0,0) with run and rise a, b.
            <a*t, b*t> """
        def x(t): return a*t
        def y(t): return b*t
        def dx(t, n=1):
            if   n==0: return t*a
            elif n==1: return a
            else:      return 0
        def dy(t, n=1):
            if   n==0: return t*b
            elif n==1: return b
            else:      return 0
        Curve.__init__(self, x, y, dx, dy)

class Circle(Curve):
    def __init__(self, r, omega=1.0, o=0.0):
        """ Parametric circle with radius `r`, angular
            velocity `omega`, and rotational offset `o`.
            <r*cos(omega*t+o), r*sin(omega*t+o)> """
        def x(t): return r*cos(omega*t+o)
        def y(t): return r*sin(omega*t+o)
        def dx(a, n=1): return omega**n * r*cosprime(n)(omega*a+o)
        def dy(a, n=1): return omega**n * r*sinprime(n)(omega*a+o)
        Curve.__init__(self, x, y, dx, dy)

################################################################################
## Special curves

class Epitrochoid(Curve):
    def __init__(self, R, r, d, o=0.0):
        """ An epitrochoid is a roulette traced by a point attached to a
            circle of radius `r` rolling around the outside of a fixed
            circle of radius `R`, where the point is at a distance `d`
            from the center of the exterior circle. `o` is the
            rotational offset of the rotating circle (0<=o<tau).
            https://en.wikipedia.org/wiki/Epitrochoid """
        r1 = R+r
        omega = float(R+r) / r
        def x(t): return r1*cos(t) - d*cos(omega*t+o)
        def y(t): return r1*sin(t) - d*sin(omega*t+o)
        def dx(t, n=1):
            cp = cosprime(n)
            return r1*cp(t) - d*omega**n*cp(omega*t+o)
        def dy(t, n=1):
            sp = sinprime(n)
            return r1*sp(t) - d*omega**n*sp(omega*t+o)
        Curve.__init__(self, x, y, dx, dy)

class Hypotrochoid(Curve):
    def __init__(self, R, r, d, o=0.0):
        """ A hypotrochoid is a roulette traced by a point attached to a
            circle of radius `r` rolling around the inside of a fixed
            circle of radius `R`, where the point is a distance `d`
            from the center of the interior circle. `o` is the
            rotational offset of the rotating circle (0<=o<tau).
            https://en.wikipedia.org/wiki/Hypotrochoid """
        r1 = R-r
        omega = float(R-r) / r
        def x(t): return r1*cos(t) + d*cos(omega*t+o)
        def y(t): return r1*sin(t) - d*sin(omega*t+o)
        def dx(t, n=1):
            cp = cosprime(n)
            return r1*cp(t) + d*omega**n*cp(omega*t+o)
        def dy(t, n=1):
            sp = sinprime(n)
            return r1*sp(t) - d*omega**n*sp(omega*t+o)
        Curve.__init__(self, x, y, dx, dy)

def Trochoid(n, r, o=0.0):
    """ Trochoid curve, simplified.
        n: Number f loops. Positive n makes epitrochoid,
                           negative n makes hypotrochoid.
        r: radius of the rolling part. (fixed part has radius 1)
        o: rotational offset of rolling part. """
    c0 = Circle(1.0)
    c1 = Circle(r, n+1, o)
    return (c0+c1)

class Lissajous(Curve):
    def __init__(self, a, b, A, B, delta):
        """ x = A * sin(a + delta)
            y = B * sin(b)
            https://en.wikipedia.org/wiki/Lissajous_curve """
        def x(t):
            return A * sin(a*t + delta)
        def y(t):
            return B * sin(b*t)
        def dx(t, n=1):
            return A * a**n * sinprime(n)(a*t + delta)
        def dy(t, n=1):
            return B * b**n * sinprime(n)(b*t)
        Curve.__init__(self, x, y, dx, dy)
