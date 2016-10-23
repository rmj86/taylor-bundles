# Example of taylor bundle rendering. "Asteriod curve" as generating curve,
# with it's 5th degree TB. First it is user-defined and rendered using the
# default, numeric differentiation. Then it's rendered with the predefined
# Trochoid class, using exact differentiation. In this case, it is evident
# that numerical differnetiation makes no appreiable difference on the
# result.

import curve
import taylorbundle
import colormix
from numpy import sin, cos, pi

tau = 2*pi  # the correct circle constant

# first, user-defined Curve with numeric differentiation

def x(t): return cos(t) + cos(-3*t) / 3.0
def y(t): return sin(t) + sin(-3*t) / 3.0
c_num = curve.Curve(x, y)

color1 = (0.2, 0.4, 1)  # clear blue
color2 = (1, 0, 0.2)    # red
mix = colormix.cosine2(color1, color2, 0, tau/4)

tb = taylorbundle.TaylorBundle(
      filename = "renders/example_asteroid_numericdiff"
    , curve = c_num
    , domain = [0, tau]
    , showcurve = False
    , degree = 5
    , window = [-4, 4, -2.25, 2.25]
    , figsize = [16,9]
    , dpi = 30
    , n_part = 8
    , n_tan = 750
    , tancol = mix
    , tanlw = 0.5
    , tanalpha = 0.4
    , tandomain = [-2,2]
    )
tb.render()

# Then, predefined curve with exact differentiation

c_exact = curve.Trochoid(-4, 1./3, 0)

tb.set_options(
      filename = "renders/example_asteroid_exactdiff"
    , curve = c_exact
    )
tb.render()

# Finally, render the color legend

tb.set_options( filename = "renders/example_asteroid" )
tb.renderTancolorLegend()