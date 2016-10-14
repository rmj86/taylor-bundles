# Example of taylor bundle rendering. Asteriod-like hypotrochoid curve, with it's 5th degree TB.

import curve
import taylorbundle
import colormix
import numpy

tau = 2 * numpy.pi

def main():
    c = curve.Trochoid(-4, 1./3, 0)
    color1 = (0.2, 0.4, 1)
    color2 = (1, 0, 0.2)
    color_f = colormix.cosine2(color1, color2, 0, tau/4)
    tb = taylorbundle.TaylorBundle(
          curve = c
        , showcurve = False
        , degree = 5
        , window = [-4, 4, -2.25, 2.25]
        , tancol = color_f
        , tanlw = 0.4
        , tanalpha = 0.2
        , n_part = 8
        # , keep_partials = True
        , filename = "renders/asteroid"
        )
    tb.render(
          # preview = True
        # , scale = 0.25
        )
    
if __name__ == "__main__":
    main()
