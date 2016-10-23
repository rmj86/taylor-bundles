# -*- coding: utf-8 -*-
"""
Taylor Bundles

Usage:
see "examples" files

Controling image saturation:
The color intensity / saturation of the image is proportional to tan_lw, tan_alpha, and n_tan, and inversely proportional to the linear size of the redered image. Keeping n_tan*tallw*tanalpha constant keeps the intensity constant at a given resolution. For full-HD res, good options are
n_tan = 2500
tanlw = 0.4
tanalpha = 0.1

Parts:
Too keep memory usage down, we can't render too many curves all at once. Therefore it's useful to split the curves between several separate partial renderings and compose the images after. n_part is the number of partial renders, and n_tan is the number of curves in each part. The final uotput is made up of n_part*n_tan curves. Good options for a perfectly smooth, "continuous-looking" result are
n_tan = 2500
n_part = 16

@author rmj86
"""

import numpy
import matplotlib
matplotlib.use("agg")
from matplotlib import pyplot
import misc
import image
import colormix
import curve
import types
from matplotlib.collections import LineCollection
from matplotlib.colors import colorConverter
import copy

tau = 2 * numpy.pi

class TaylorBundle:
    __opts = { "curve", "n_part", "n_tan", "degree"
             , "domain", "curvedomain", "bundledomain"
             , "figsize", "dpi", "window", "facecolor"
             , "showcurve", "curveres", "curvecol", "curvelw"
             , "curvealpha", "tandomain", "tanres", "tancol"
             , "tanlw", "tanalpha", "filename", "keep_partials"
             }
    curve = None
    n_part = 1               # number of partial images to render
    n_tan = 200              # number of tangents per partial image
    degree = 1               # polynomial degree of tangents
    domain = (0, tau)        # domain of curve and tangent space
    curvedomain = (0, tau)   # domain of generating curve
    bundledomain = (0, tau)  # domain of tangent bundle
    figsize = (16,9)         # size of image (in inches)
    dpi = 30                 # dpi of image
    window = [-16,16,-9,9]   # bounds of the plotting surface
    facecolor = 'k'          # background colour of plotting surface
    showcurve = True  # show the generating curve on top of the tangent bundle
    curveres = 256           # resolution of generating curve
    curvecol = "w"           # colour of generating curve
    curvelw = 2              # line width of generating curve
    curvealpha = None        # transparency of generating curve
    tandomain = [-2, 2]      # domain of tangent polynomial (around the point of tangency)
    tanres = 256             # resolution of tangent curves
    tancol = "r"  # colour of tangents. Can be constant or generating function
    tanlw = 1                # line width of tangents
    tanalpha = None          # tranparency of tangents
    filename = None          # file name to save to. Defaults to date and time
    keep_partials = False    # keep partial files after render finishes
    def __init__(self, **options):
        self.set_options(**options)
    def set_options(self, **options):
        for o,v in options.items():
            if o not in self.__opts:
                print "WARNING: Unknown option {}".format(o)
            if o == "domain":
                setattr(self, "curvedomain", v)
                setattr(self, "bundledomain", v)
            setattr(self, o, v)
    def initializeFigure(self, figsize):
        """ initialize the plotting surface """
        fig = pyplot.gcf()
        fig.set_size_inches(*figsize)
        fig.set_dpi(self.dpi)
        ax = pyplot.gca()
        ax.set_position([0,0,1,1])
        return fig
    def initializeAxes(self):
        """ clear and set properties of current axes """
        ax = pyplot.gca()
        ax.clear()
        ax.axis(self.window)
        ax.axis("off")
        return ax
    # @timed(showargs=False)
    def drawTangents(self, ax, tmin, tmax, n_tan):
        # function paramter values
        t = numpy.linspace(tmin, tmax, n_tan, False)
        t = misc.permute(t)
        # color array
        cmix = colormix.fromConstant(self.tancol)
        colors = cmix(t)
        # plot the tangents on current axis
        (amin, amax) = self.tandomain
        for a, c in zip(t, colors):
            p = self.curve.taylorCurve(a, self.degree)
            s = numpy.linspace(a+amin, a+amax, self.tanres)
            ax.plot( p.x(s), p.y(s), color=c, zorder=0
                       , linewidth=self.tanlw, alpha=self.tanalpha )

    def drawCurve(self, ax):
        # print "drawing"
        # return
        # print repr(self._drawCurve_constcolor)
        if type(self.curvecol) == types.FunctionType:
            self._drawCurve_varColor(ax)
        else:
            self._drawCurve_constColor(ax)

    def _drawCurve_constColor(self, ax):
        # pass
        tmin, tmax = self.curvedomain
        t = numpy.linspace(tmin, tmax, self.curveres)
        ax.plot(
              self.curve.x(t)
            , self.curve.y(t)
            , color = self.curvecol
            , lw = self.curvelw
            , alpha = self.curvealpha
            , zorder = 1
            )
    def _drawCurve_varColor(self, ax):
        tmin, tmax = self.curvedomain
        t = numpy.linspace(tmin, tmax, self.curveres)
        x = self.curve.x(t)
        y = self.curve.y(t)
        coords = numpy.ndarray((self.curveres-1, 2, 2))
        coords[:,0,0] = x[:-1]
        coords[:,1,0] = x[1:]
        coords[:,0,1] = y[:-1]
        coords[:,1,1] = y[1:]
        colors = self.curvecol(t)
        segments = LineCollection( coords
                                 , colors = colors[:-1]
                                 , lw = self.curvelw
                                 , alpha = self.curvealpha
                                 , zorder = 1 )
        ax = pyplot.gca()
        ax.add_collection(segments)

    @misc.timed(False)
    def render(self, preview=False, scale=0.25):
        filename, figsize = self.filename, self.figsize,
        n_part, n_tan = self.n_part, self.n_tan
        tmin, tmax = self.bundledomain
        # initialize filename
        if not type(filename) == str:
            filename = misc.datetimeFilename(pre="taylorbundle_render_")
        # initialize preview options
        if preview:
            n_part = max(1, int(scale * n_part))    # must be int >= 1
            figsize = (scale * figsize[0], scale * figsize[1])
            n_tan = int(scale * n_tan)
            filename = "{}_preview{}".format(filename, scale)

        # set up the ploting surface
        fig = self.initializeFigure(figsize)
        # render partials
        # --------
        # div by zero quick fix: set dt to an arbitrary value if zero n_tan
        if n_tan == 0: dt = 1
        else: dt = float(tmax-tmin)/n_tan
        ds = numpy.linspace(0, dt, n_part, False)
        partial_filenames = []
        for i, d in enumerate(ds):
            ax = self.initializeAxes()  # clear the current axes
            self.drawTangents(ax, tmin+d, tmax+d, n_tan)
            # plot the curve
            if self.showcurve:
                self.drawCurve(ax)
            pfname = "{}_partial{}.png".format(filename, i)
            fig.savefig(pfname, dpi = self.dpi, facecolor = self.facecolor)
            partial_filenames.append(pfname)
        # compose partials and delete partial files
        image.composeAverage(filename+".png", partial_filenames)
        if not self.keep_partials:
            for fn in partial_filenames:
                misc.deleteFile(fn)
