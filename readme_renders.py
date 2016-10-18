# renders the images used in README.md

import taylorbundle
import curve
from numpy import (sin, cos, pi)
from copy import copy

####################
##  Tangent bundle

wx = 4*pi
wy = wx * 9./16
tb1 = taylorbundle.TaylorBundle(
          curve = curve.fromFunction(sin)
        , window = [-wx, wx, -wy, wy]
        , domain = [-wx, wx]
        , curvelw = 6
        , tanlen = 30
        , dpi = 30
        )

def fig1():
    tb = copy(tb1)
    tb.set_options(
              filename = "figures/readme_fig1"
            , n_tan = 1
            , bundledomain = [1,1]
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

##########################################
##  2nd degree taylor bundle

tb2 = copy(tb1)
tb2.set_options( degree = 2 )

def fig4():
    tb = copy(tb2)
    tb.set_options(
              filename = "figures/readme_fig4"
            , n_tan = 1
            , bundledomain = [1,1]
            , tanlw = 4
            , tanalpha = 1
            )
    tb.render()

def fig5():
    tb = copy(tb2)
    tb.set_options(
              filename = "figures/readme_fig5"
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
    fig4()
    fig5()
