# -*- coding: utf-8 -*-
"""
Taylor Bundles

Usage: See README.md

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

class TaylorBundle(object):
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
    curvelw = 6              # line width of generating curve
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
            setattr(self, o, v)
    def __setattr__(self, attr, value):
        if not hasattr(self, attr):
            raise AttributeError('TaylorBundle has no attribute "{}"'.format(attr))
        if attr == "domain":
            self.curvedomain  = value
            self.bundledomain = value
        object.__setattr__(self, attr, value)
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
        # calculate taylor curves' coordinates
        taylorcoords = numpy.ndarray((n_tan, self.tanres, 2))
        (amin, amax) = self.tandomain
        for i, a in enumerate(t):
            s = numpy.linspace(a+amin, a+amax, self.tanres)
            p = self.curve.taylorCurve(a, self.degree)
            taylorcoords[i,:,0] = p.x(s)
            taylorcoords[i,:,1] = p.y(s)
        # taylor curve collection
        taylorcurves = LineCollection( taylorcoords
                                     , colors = colors
                                     , lw = self.tanlw
                                     , alpha = self.tanalpha
                                     , zorder = 0 )
        # add collection to current axes
        ax.add_collection(taylorcurves)

    def drawCurve(self, ax):
        if type(self.curvecol) == types.FunctionType:
            self._drawCurve_varColor(ax)
        else:
            self._drawCurve_constColor(ax)

    def _drawCurve_constColor(self, ax):
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

    def renderTancolorLegend(self):
        tb = copy.copy(self)
        tb.set_options(
              showcurve=True
            , curvecol = self.tancol
            , n_tan = 0 )
        if type(self.filename) == str:
            tb.set_options( filename = self.filename + "_tancolorLegend")
        else:
            tb.set_options( filename = misc.datetimeFilename("taylorbundle_tancolorLegend_") )
        tb.render()
