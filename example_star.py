# Example render of Taylor bundle. 5-sided "squished circle" generating
# curve (hypotrochoid). Pentagram-like TB. A4 figure size. Can be used as
# a tasteful watermark on paper.

import curve
import taylorbundle
import colormix
from numpy import pi, sqrt

tau = 2 * pi

c = curve.Trochoid(-5, r= 14./240)
color1 = (1, 0.2, 0.1) # lightish red
color2 = (0.2, 0, 0)   # reddish black
# periodic gradient with color1 around t=0 and color2 around t=tau/10
mix = colormix.cosine2(color1, color2, 0, tau/10)
tb = taylorbundle.TaylorBundle(
      curve = c
    , filename = "renders/example_star"
    , showcurve = False
    , window = [-5/sqrt(2), 19/sqrt(2), -4, 20]
    , figsize = [8.267, 11.692]   # size of an A4 paper
    , facecolor = 'w'
    , n_part = 8
    , n_tan = 500
    , tancol = mix
    , tanlw = 0.5
    , tanalpha = 0.4
    , tandomain = [-24, 24]
    , degree = 2
    , dpi = 30
    )

tb.renderTancolorLegend()
tb.render()