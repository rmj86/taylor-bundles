# renders the images used in README.md

import taylorbundle
import curve
import colormix
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

####################
##  Trochoid curve

o = pi/4  # rotational offset of curve, in radians
curve_troch = curve.Trochoid(4, 0.8, 4*o)
# c_mix = colormix.cosine2((0,0.7,0.2), (1,0,0.1), o+0, o+pi/4, linear=True)
c_mix = colormix.cosine2("gold", "dodgerblue", o+0, o+pi/4, linear=True)
tb3 = copy(tb1)
tb3.set_options(
          curve = curve_troch
        , domain = (0, 2*pi)
        , window = [-4, 4, -2.25, 2.25]
        , n_tan = 1000
        , n_part = 10
        , tanlw = 0.8
        , tanalpha = 0.3
        , degree = 4
        , tanlen = 1
        )

def fig6():
    tb = copy(tb3)
    tb.set_options(
              filename = "figures/readme_fig6"
            , n_tan = 1
            , n_part = 1
            , bundledomain = [1,1]
            , tanlw = 4
            , tanalpha = 1
            )
    tb.render()

def fig7():
    tb = copy(tb3)
    tb.set_options(
              filename = "figures/readme_fig7"
            )
    tb.render()

def fig8():
    tb = copy(tb3)
    tb.set_options(
              filename = "figures/readme_fig8"
            , n_tan = 0
            , n_part = 1
            , curvecol = c_mix
            )
    tb.render()

def fig9():
    tb = copy(tb3)
    tb.set_options(
              filename = "figures/readme_fig9"
            , showcurve = False
            , tancol = c_mix
            )
    tb.render()


if __name__ == "__main__":
    fig1()
    fig2()
    fig3()
    fig4()
    fig5()
    fig6()
    fig7()
    fig8()
    fig9()
