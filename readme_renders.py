# renders the images used in README.md

import taylorbundle
import curve
from numpy import (sin, cos, pi)
from copy import copy

wx = 8*pi
wy = wx * 9./32
tb1 = taylorbundle.TaylorBundle( 
          curve = curve.fromFunction(sin)
        , window = [0, wx, -wy, wy]
        , domain = [0,8*pi]
        , curvelw = 6
        , tanlen = 30
        , dpi = 30
        )

def fig1():
    tb = copy(tb1)
    tb.set_options(
              filename = "figures/readme_fig1"
            , n_tan = 4
            , tanlw = 4
            , tanalpha = 1
            )
    tb.render()

def fig2():
    tb = copy(tb1)
    tb.set_options(
              filename = "figures/readme_fig2"
            , n_tan = 200
            , tanlw = 4
            , tanalpha = 0.5
            )
    tb.render()

def fig3():
    tb = copy(tb1)
    tb.set_options(
              filename = "figures/readme_fig3"
            , n_tan = 1000
            , n_part = 10
            , tanlw = 1
            , tanalpha = 0.4
            )
    tb.render()

if __name__ == "__main__":
    fig1()
    fig2()
    fig3()
