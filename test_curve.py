
import curve as c
import numpy as np
from tests import testAll
tau = 2 * np.pi

################################################################################
## Utility functions
def verySmall(a, delta=1e-30):
    """ returns True when the values of ndarray `a` are small. """
    # used when we really want the values to be 0, but this
    # can't be guaranteed due to floating errors.
    return np.average(a*a) <= delta



################################################################################
# numDiff tests
def t_numDiff_sin():
    v = c.numDiff(np.sin, np.pi, 1)
    expected = -1
    return verySmall(v-expected,  1e-8)
def t_numDiff_sin5():
    v = c.numDiff(np.sin, np.pi, 1)
    expected = -1
    return verySmall(v-expected,  1e-8)

################################################################################
# taylorPoly tests
def t_taylorPoly_cos():
    p = c.taylorPoly(np.cos, 0, n=2)
    v = p(np.arange(4))
    v_ = [1, 0.5, -1, -3.5]
    return verySmall(v-v_, 1e-8)
def t_taylorPoly_sin():
    def d_sin(a,n):
        return c.sinprime(n)(a)
    p = c.taylorPoly(np.sin, 0, n=3, df=d_sin)
    v = p(np.arange(4))
    v_ = [0, 5./6, 2./3, -3./2]
    return verySmall(v-v_)

################################################################################
# sinprime and cosprime tests
def t_sinprime():
    v = [c.sinprime(n)(0) for n in range(8)]
    v_ = np.array([0,1,0,-1,0,1,0,-1])
    return verySmall(v-v_)
def t_cosprime():
    v = [c.cosprime(n)(0) for n in range(8)]
    v_ = np.array([1,0,-1,0,1,0,-1,0])
    return verySmall(v-v_)

################################################################################
# Curve tests
def t_curve_base_case():
    circ = c.Curve(np.cos, np.sin)
    t = np.linspace(0,tau,5)
    xs = circ.x(t)
    ys = circ.y(t)
    xs_ = [1,0,-1,0,1]
    ys_ = [0,1,0,-1,0]
    return (verySmall(xs-xs_) and verySmall(ys-ys_))
def t_curve_call():
    circ = c.Curve(np.cos, np.sin)
    t = np.linspace(0,tau,5)
    ps = circ(t)
    ps_ = [[1,0],[0,1],[-1,0],[0,-1],[1,0]]
    return verySmall(ps-ps_)
def t_curve_taylorCurve():
    circ = c.Curve(np.cos, np.sin)
    poly = circ.taylorCurve(tau/2, n=3)
    t = np.linspace(tau/2-1,tau/2+1,3)
    ps = poly(t)
    ps_ = [[-.5,5./6],[-1, 0],[-.5,-5./6]]
    return verySmall(ps-ps_, 1e-8)
def t_curve_dxdydt():
    @ np.vectorize
    def dt(a,n): return n
    circ = c.Curve(np.cos, np.sin, dx=dt, dy=dt)
    poly = circ.taylorCurve(1, n=2)
    t = np.array([0,1,2,3,4])
    ps = poly(t)
    ps_ = [[0,0],[0,0],[2,2],[6,6],[12,12]]
    return verySmall(ps-ps_)
def t_curve_add():
    circ = c.Curve(np.cos, np.sin)
    line = c.Curve(lambda t: 4*t/tau, lambda t: 8*t/tau)
    spiral = circ+line
    t = np.linspace(0,tau,5)
    ps = spiral(t)
    ps_ = [[1,0],[1,3],[1,4],[3,5],[5,8]]
    return verySmall(ps-ps_)
    
################################################################################
# fromFunction tests

################################################################################
# Point tests

################################################################################
# Line tests

################################################################################
# Circle tests

################################################################################
# Epitrochoid tests

################################################################################
# Hypotrochoid tests

################################################################################
# Lissajous tests

################################################################################
# all tests

all_tests = [
              t_numDiff_sin
            , t_numDiff_sin5
            , t_taylorPoly_cos
            , t_taylorPoly_sin
            , t_sinprime
            , t_cosprime
            , t_curve_base_case
            , t_curve_call
            , t_curve_taylorCurve
            , t_curve_dxdydt
            , t_curve_add
            ]
            
if __name__ == "__main__":
    testAll( all_tests)