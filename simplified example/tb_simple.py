# barebones example of TB rendering stripped of extraneous abstractions 
# for easier profiling and experimentation with optimizations 

import matplotlib
matplotlib.use("agg")
from matplotlib import pyplot
from matplotlib.collections import LineCollection
import numpy
from numpy import pi, sin, cos, sqrt, ndarray, linspace, array, newaxis
import numexpr

###############################################################################
## Render settings

# taylor poly properties
n_tan     = 5000    # how many polynomial curves
tan_res   = 1024    # how many coordinate points per poly
tan_span  = 8       # span of poly curve around the point of tangency
tan_lw    = 0.25    # line width of poly curve
tan_alpha = 0.2     # opacity of poly curve

# figure properties
zoom = 3
fig_size    = (16,9)
fig_dpi     = 80
fig_window  = [-zoom*16,zoom*16,-zoom*9,zoom*9]
fig_bgcolor = 'k'

filename = "tb_simple.png"

###############################################################################
## Calculating the curves. Taylor polynomials of order 2 
## on a (12,1) epitrochoid 

# points of tangency for the Taylor Polynomial curves
t = linspace(0, 2*pi, n_tan, endpoint=False)

d = 1. / 11.  ## eccentricity of epitrochoid 

# parametric curve points and derivatives of order 1, 2
def generating_curve():
    x   =  13*cos(t) - d*    cos(13*t)
    dx  = -13*sin(t) + d* 13*sin(13*t)
    d2x = -13*cos(t) + d*169*cos(13*t)
    y   =  13*sin(t) - d*    sin(13*t)
    dy  =  13*cos(t) - d* 13*cos(13*t)
    d2y = -13*sin(t) + d*169*sin(13*t)
    return (x,dx,d2x,y,dy,d2y)

# coeffs of Taylor poly curves   |   shape (n, 2, 3)
def taylor_polys():
    (x,dx,d2x,y,dy,d2y) = generating_curve()
    polys = ndarray((n_tan,2,3)) # index order: curve, x/y, coeff of 1/a/a**2
    polys[:,0,0] = x - t*dx + .5*t**2*d2x
    polys[:,0,1] = dx - t*d2x
    polys[:,0,2] = .5*d2x
    polys[:,1,0] = y - t*dy + .5*t**2*d2y
    polys[:,1,1] = dy - t*d2y
    polys[:,1,2] = .5*d2y
    return polys

# parameter values for taylor polys
def taylorcurve_params():
    _params = linspace(-tan_span, tan_span, tan_res)
    params = _params + t[:,newaxis]  # shape (n, r) : (corresponding poly, parameter value)
    return params

# curve coordinates of taylor polys
def taylorcurve_coords():
    p = taylor_polys()
    a = taylorcurve_params()
    # evaluating the polys at the parameter values
    # broadcasting shapes of p and a:
    #    n _ 2 3    p
    #  , n r _      a
    # -> n r 2      (point coordinates of the curves )
    p.shape = (n_tan,       1, 2, 3)   # for broadcasting
    a.shape = (n_tan, tan_res, 1)      # for broadcasting
    p0, p1, p2 = p[...,0], p[...,1], p[...,2]
    coords = numexpr.evaluate("p0 + a*(p1 + a*p2)")
    return coords

###############################################################################
## Plotting

# curve colors
def taylorcurve_colors():
    c0 = array([.4, .8,  1, tan_alpha])  # light blue
    c1 = array([ 1, .8, .3, tan_alpha])  # yellow
    w = 0.5*(1-cos(12*t))     # weighting of c1 / c2
    w.shape = (n_tan, 1)      # for broadcasting
    colors = sqrt( (1-w)*c0**2 + w*c1**2 )  # weighted average in linear color space
    return colors

# making line collection
lines = LineCollection(taylorcurve_coords(), lw=tan_lw, 
                       colors=taylorcurve_colors())

# setting up plotting surface
fig = pyplot.gcf()
fig.set_size_inches(*fig_size)
ax = pyplot.gca()
ax.set_position([0,0,1,1])
ax.axis(fig_window)
ax.axis("off")

# adding lines and saving image file
ax.add_collection(lines)
fig.savefig(filename, dpi=fig_dpi, facecolor=fig_bgcolor)
print "saved file: {}".format(filename)

#DONE!
