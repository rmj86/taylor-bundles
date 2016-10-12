# Example render of Taylor bundle. Pentagram-like

import curve
import taylorbundle
import colormix
from numpy import pi, sqrt

tau = 2 * pi

def main():
    c = curve.Trochoid(-5, r= 14./240)
    color1 = (1, 0.2, 0.2)
    color2 = (0.4, 0.0, 0.2)
    color_f = colormix.cosine2(color1, color2, 0, tau/10)
    tb = taylorbundle.TaylorBundle(
          curve = c
        , showcurve = False
        , degree = 2
        , window = [-5/sqrt(2), 19/sqrt(2), -4, 20]
        , figsize = [8.267, 11.692]
        , facecolor = 'w'
        , tancol = color_f
        , tanlen = 24
        , n_part = 1
        , filename = "renders/example_star"
        )

    tb.render( 
          # preview = True
        # , scale = 0.25
        )
    
if __name__ == "__main__":
    main()
