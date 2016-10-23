import taylorbundle
import colormix
import curve
import numpy

c = curve.Lissajous(5, 3, 3./5, 5./5, numpy.pi/4)

# By default the color mixer is passed the curve parameter values as an
# argument. Here we set up a custom function that instead calculates the
# color as a function of the curve's x values.
def mix(t):
    (xmin, xmax) = (-3./5, 3./5)  # the min and max bounds of x
    delta = xmax - xmin
    # first, make a red-to-blue color gradient from xmin to xmax
    mix_gradient = colormix.mix2("r", "b", colormix.cosine(xmin, xmax))
    # on top of that, make a peak of gold around x=0 with width delta/6
    mix_peak = colormix.mix2(mix_gradient, "gold",
                             colormix.gaussian(0, delta/3))
    # apply the mixer to the x values of the
    # curve instead of the parameter values
    colors = mix_peak( c.x(t) )
    return colors

# set the TB properties
tb = taylorbundle.TaylorBundle(
      curve = c
    , filename = "renders/example_lissajous"
    , window = [-4, 4, -2.25, 2.25]
    , figsize = [16, 9]
    , dpi = 30
    , showcurve = False
    , n_part = 8
    , n_tan = 500
    , tancol = mix
    , tanalpha = 0.4
    , tanlw = 0.5
    , tandomain = [-1, 1]
    , degree = 7
    )

# render a legend for the tangent coloring
tb.renderTancolorLegend()
# render the Taylor bundle
tb.render()
