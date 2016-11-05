
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
# const tests
def t_aconst_dtype():
    t = np.arange(6)
    f = c.aconst(77)
    x = f(t)
    return (x.dtype == np.float64)
def t_aconst_values():
    t = np.arange(6)
    f = c.aconst(77.5)
    x = f(t)
    x_ = x - 77.5
    return (x_ == 0).all()

################################################################################
# fromFunction tests
def t_fromFunction_dtype():
    pcurve = c.fromFunction(lambda x: x)
    t = np.arange(5, dtype=np.int32)#, dtype=np.float64)
    ps = pcurve(t)
    return ps.dtype == np.float64
def t_fromFunction_values():
    pcurve = c.fromFunction(lambda x: x*x*x)
    t = np.arange(5)
    ps = pcurve(t)
    ps_ = [[0,0],[1,1],[2,8],[3,27],[4,64]]
    return verySmall(ps-ps_)

################################################################################
# Point tests
def t_point_values():
    point = c.Point(3,5)
    t = np.linspace(1,77,3)
    ps = point(t)
    ps_ = [[3,5],[3,5],[3,5]]
    return (ps==ps_).all()
def t_point_diff():
    point = c.Point(3,5)
    ds = np.array( [ point.dx(99, n=0)
                   , point.dy(99, n=0)
                   , point.dx(99, n=1)
                   , point.dy(99, n=1)
                   , point.dx(99, n=2)
                   , point.dy(99, n=2) ]
                 , dtype = np.float64)
    expected = np.array([3,5,0,0,0,0])
    return (expected == ds).all()

################################################################################
# Line tests
def t_line_values():
    line = c.Line(2,6)
    t = np.arange(4)
    ps = line(t)
    ps_ = [[0,0],[2,6],[4,12],[6,18]]
    return verySmall(ps-ps_)
def t_line_diff():
    line = c.Line(2,6)
    ds = np.array( [ line.dx(0,  n=0)
                   , line.dx(10, n=0)
                   , line.dx(0,  n=1)
                   , line.dx(1,  n=2)
                   , line.dy(0,  n=0)
                   , line.dy(10, n=0)
                   , line.dy(0,  n=1)
                   , line.dy(1,  n=2) ]
                 , dtype=np.float64)
    expected = np.array([0,20,2,0,  0,60,6,0])
    return (expected == ds).all()

################################################################################
# Circle tests
def t_circle_values():
    circ = c.Circle(5, 2, tau/4)
    t = np.linspace(0,tau/2,5)
    ps = circ(t)
    t_ = np.linspace(0,tau,5)
    ps_ = [[0,5],[-5,0],[0,-5],[5,0],[0,5]]
    return verySmall(ps-ps_)
def t_circle_diff():
    circ = c.Circle(5, 2, tau/4)
    ds = np.array( [ circ.dx(0, n=0)
                   , circ.dx(0, n=1)
                   , circ.dx(0, n=2)
                   , circ.dy(0, n=0)
                   , circ.dy(0, n=1)
                   , circ.dy(0, n=2) ]
                 , dtype = np.float64 )
    expected = [0,-10,0,5,0,-20]
    return verySmall(ds-expected)

################################################################################
# Primitive curve add tests
def t_curve_add_point_line_values():
    pt = c.Point(5,10)
    ln = c.Line(2,5)
    shifted_ln = pt + ln
    t = np.arange(5)
    ps = shifted_ln(t)
    ps_ = np.array([[5,7,9,11,13],[10,15,20,25,30]]).T
    return verySmall(ps-ps_)
def t_curve_add_circ_circ_values():
    c1 = c.Circle(1,1,0)
    c2 = c.Circle(2,2,0)
    c3 = c1+c2
    t = np.linspace(0,tau,5)
    ps = c3(t)
    ps_ = np.array([[3,-2,1,-2,3], [0,1,0,-1,0]]).T
    return verySmall(ps-ps_)
def t_curve_add_circ_circ_diff():
    c1 = c.Circle(1,1,0)
    c2 = c.Circle(2,2,0)
    c3 = c1+c2
    t = np.linspace(0,tau,5)
    dx = c3.dx(t)
    dy = c3.dy(t)
    dx_ = [0,-1,0,1,0]
    dy_ = [5,-4,3,-4,5]
    return (verySmall(dx-dx_,1e-29) and verySmall(dy-dy_))

################################################################################
# Epitrochoid tests
def t_epitrochoid_values():
    epi = c.Epitrochoid(3,1,2,tau/2)
    t = np.linspace(0, tau/3, 5)
    pts = epi(t)
    sq3 = np.sqrt(3)
    pts_ = np.array( [ [6      , 0    ]
                   , [2*sq3-1, sq3+2]
                   , [1      , sq3  ]
                   , [2      , 4    ]
                   , [-3     , 3*sq3] ]
                 , dtype = np.float64 )
    return verySmall(pts-pts_, 2e-30)

def t_epitrochoid_taylor_curve():
    epi = c.Epitrochoid(3,1,2,tau/2)
    a = tau/4
    poly = epi.taylorCurve(a, n=2)
    poly_ = c.Curve( x = lambda t: 2 - 4*(t-a) - 16*(t-a)**2
                   , y = lambda t: 4 + 8*(t-a) -  2*(t-a)**2 )
    t = np.linspace(0,3,11)
    pts  = poly(t)
    pts_ = poly_(t)
    return verySmall(pts-pts_, 1e-28)

################################################################################
# Hypotrochoid tests
def t_hypotrochoid_values():
    hypo = c.Hypotrochoid(3, 1, 2, tau/2)
    t = np.linspace(0, tau/3, 5)
    pts = hypo(t)
    sq3 = np.sqrt(3)
    pts_ = np.array( [ [0    , 0    ]
                   , [sq3-1, sq3+1]
                   , [2    , 2*sq3]
                   , [2    , 2    ]
                   , [0    , 0    ] ]
                 , dtype = np.float64 )
    return verySmall(pts-pts_, 2e-30)

def t_hyporochoid_taylor_curve():
    hypo = c.Hypotrochoid(3,1,2,tau/2)
    a = tau/4
    poly = hypo.taylorCurve(a, n=2)
    poly_ = c.Curve( x = lambda t: 2 - 2*(t-a) - 4*(t-a)**2
                   , y = lambda t: 2 - 4*(t-a) - 1*(t-a)**2 )
    t = np.linspace(0,3,11)
    pts  = poly(t)
    pts_ = poly_(t)
    return verySmall(pts-pts_, 1e-28)

################################################################################
# Lissajous tests
def t_lissajous_values():
    liss = c.Lissajous(3, 4, 4, 3, tau/12)
    t = np.linspace(0, tau/3, 5)
    pts = liss(t)
    sq3 = np.sqrt(3)
    pts_ = np.array( [ [2      , 0       ]
                     , [2*sq3  , 3*sq3/2 ]
                     , [-2     , -3*sq3/2]
                     , [-2*sq3 , 0       ]
                     , [2      , 3*sq3/2 ] ]
                   , dtype = np.float64 )
    return verySmall(pts-pts_)

def t_lissajous_taylor_curve():
    liss = c.Lissajous(3, 4, 4, 3, tau/12)
    a = 2*tau/12
    sq3 = np.sqrt(3)
    poly = liss.taylorCurve(a, n=2)
    poly_ = c.Curve( x = lambda t: -2       - 6*sq3*(t-a) + 9     *(t-a)**2
                   , y = lambda t: -3*sq3/2 - 6    *(t-a) + 12*sq3*(t-a)**2 )
    t = np.linspace(0, 3, 11)
    pts  = poly(t)
    pts_ = poly_(t)
    return verySmall(pts-pts_, 1e-27)

################################################################################
# all tests
all_tests = [ value
              for name, value in locals().items()
              if name.startswith("t_")
            ]

if __name__ == "__main__":
    testAll(all_tests, v=3)
