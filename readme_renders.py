# renders the images used in README.md

import taylorbundle
import curve
from numpy import (sin, cos, pi)

x = lambda t: t
f = lambda t: sin(t)
c = curve.Curve(x, f)
tb1 = taylorbundle.TaylorBundle( curve = c )

def fig1():
    tb1.set_options( filename = "readme_fig1_4tan"
                   , n_tan = 4
                   , window = [0, 16, -4.5, 4.5]
                   , domain = [0,18]
                   , curvelw = 6
                   , tanlw = 4
                   , tanalpha = 1
                   , tanlen = 20
                   , dpi = 30
                   )
    tb1.render()

def fig2():
    wx = 8*pi
    wy = wx * 9./32
    tb1.set_options( filename = "readme_fig2_400tan"
                   , n_tan = 400
                   , window = [0, wx, -wy, wy]
                   , domain = [0,8*pi]
                   , curvelw = 6
                   , tanlw = 2
                   , tanalpha = 0.4
                   , tanlen = 20
                   , dpi = 30
                   )
    tb1.render()

def fig3():
    wx = 8*pi
    wy = wx * 9./32
    tb1.set_options( filename = "readme_fig3_20000tan"
                   , n_tan = 1000
                   , n_part = 20
                   , window = [0, wx, -wy, wy]
                   , domain = [0,8*pi]
                   , curvelw = 6
                   , tanlw = 01
                   , tanalpha = 0.4
                   , tanlen = 20
                   , dpi = 30
                   )
    tb1.render()

if __name__ == "__main__":
    fig1()
    fig2()
    fig3()