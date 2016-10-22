import taylorbundle
import colormix
import curve
import numpy

c = curve.Lissajous(5, 3, 3./5, 5./5, numpy.pi/4)

# by default the color mixer is passed 
def mix(t):
    x = c.x(t)   # the x values of the curve
    (xmin, xmax) = (-3./5, 3./5)  # the min and max bounds of x
    delta = xmax - xmin
    # first, make a red-to-blue color gradient from xmin to xmax
    mix_gradient = colormix.cosine2("r", "b", xmin, xmax)
    # on top of that, make a peak of gold around x=0 with width delta/6
    mix_peak = colormix.gaussian("gold", mix_gradient, 0, delta/6)
    # apply the mixer to the x values of the
    # curve instead of the parameter values
    colors = mix_peak( c.x(t) )
    return colors

# set up and render a legend for the coloring
tb = taylorbundle.TaylorBundle(
      curve = c
    , filename = "renders/example_lissajous_colorlegend"
    , window = [-4, 4, -2.25, 2.25]
    , figsize = [16, 9]
    , showcurve = True
    , curvelw = 6
    , curvecol = mix
    , n_tan = 0
    , dpi = 30
    )
tb.render()

# set up and render the Taylor bundle
tb.set_options(
      filename = "renders/example_lissajous_k"
    , showcurve = False
    , n_part = 8
    , n_tan = 500
    , tancol = mix
    , tanalpha = 0.4
    , tanlw = 0.5
    , tandomain = [-1, 1]
    , degree = 7
    )
tb.render()
