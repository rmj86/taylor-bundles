# renders the images used in README.md

import taylorbundle
import curve
import colormix
from numpy import (sin, cos, pi)
import numpy as np
from copy import copy
import matplotlib
import matplotlib.pyplot as plt

####################
##  Tangent bundle

wx = 4*pi
wy = wx * 9./16
tb1 = taylorbundle.TaylorBundle(
          curve = curve.fromFunction(sin)
        , window = [-wx, wx, -wy, wy]
        , domain = [-wx, wx]
        , curvelw = 6
        , tandomain = [-30, 30]
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
            , n_tan = 2000
            , n_part = 5
            , tanlw = 0.4
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
c_mix = colormix.mix2("gold", "dodgerblue", 
                      colormix.cosine(o+0, o+pi/4), linear=True)
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
        , tandomain = [-1, 1]
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

################################################################################
### colormix illustrations

def cm_fig_template(norm, normargs, filename):
    # initialize
    fig, (ax1, ax2) = plt.subplots(2, sharex = True)
    fig.subplots_adjust(hspace=0)  # no space between subplots
    ax2.get_yaxis().set_visible(False)  # remove yaxis on lower subplot
    n = 128
    t = np.linspace(0,10, n)
    c1, c2 = "royalblue", "gold"
    _norm = norm(*normargs)
    cmap = colormix.mix2(c1, c2, _norm)
    ax1.set_title("mix2({}, {}, {}{})".format(c1, c2, norm.__name__, normargs))
    # plot upper graph - the norm curve
    ax1.fill_between(t, _norm(t), 1, facecolor=c1, lw=0)
    ax1.fill_between(t, 0, _norm(t), facecolor=c2, lw=0)
    # plot lower graph - the color gradient
    colors = cmap(t)
    # vertices = np.vstack([t[:-1],t[1:]]).T[np.newaxis,:]
    vertices = np.ndarray((n-1,2,2))
    vertices[:,0,0] = t[:-1]  # x coodr pt 1
    vertices[:,1,0] = t[1:]  # x coord pt 2
    vertices[:,:,1] = 0.5
    segments = matplotlib.collections.LineCollection(vertices
                    , color=colors, lw=2*72)
    ax2.add_collection(segments)
    # save figure
    fig.set_size_inches(6,3)
    fig.savefig("figures/"+filename, dpi=60)
    plt.clf()

def cm_fig1():
    def normalize(a, b):
        def _normalize(t):
            return colormix._bounded(colormix.normalize(a,b)(t))
        return _normalize
    cm_fig_template(normalize, (2,8), "cm_fig1.png")
def cm_fig2():
    cm_fig_template(colormix.smoothstep, (2,8), "cm_fig2.png")
def cm_fig3():
    cm_fig_template(colormix.cosine, (4,6), "cm_fig3.png")
def cm_fig4():
    cm_fig_template(colormix.gaussian, (6,2), "cm_fig4.png")

def cm_fig5():
    c = curve.fromFunction( np.sin )
    def norm(t):
        return colormix.normalize(-1,1)(sin(t))
    cfun = colormix.colormap("Spectral", norm)
    tb = copy(tb1)
    tb.set_options(
              filename = "figures/cm_fig5"
            , curve = c
            , tancol = cfun
            , showcurve = False
            , n_tan = 3333
            , n_part = 3
            , tanlw = .5
            , tanalpha = 0.2
            , figsize = [6,4]
            , window = [-12,12,-8,8]
            , domain = [-20,20]
            , dpi = 60
            )
    tb.renderTancolorLegend()
    tb.render()
    

if __name__ == "__main__":
    # fig1()
    # fig2()
    # fig3()
    # fig4()
    # fig5()
    # fig6()
    # fig7()
    # fig8()
    # fig9()
    
    # cm_fig1()
    # cm_fig2()
    # cm_fig3()
    # cm_fig4()
    cm_fig5()
