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

tau = 2 * numpy.pi

class TaylorBundle:
    curve = None
    n_part = 1               # number of partial images to render
    n_tan = 2500             # number of tangents per partial image
    degree = 1               # polynomial degree of tangents
    domain = (0, tau)        # domain of curve and tangent space
    figsize = (16,9)         # size of image (in inches)
    dpi = 120                # dpi of image
    window = [0, tau, -2, 2] # bounds of the plotting surface
    facecolor = 'k'          # background colour of plotting surface
    showcurve = True  # show the generating curve on top of the tangent bundle
    curveres = 256           # resolution of generating curve
    curvecol = "w"           # colour of generating curve
    curvelw = 2              # line width of generating curve
    curvealpha = 1.0         # transparency of generating curve
    tanlen = 2               # +-length of (domain of) tangent curves
    tanres = 256             # resolution of tangent curves
    tancol = "r"  # colour of tangents. Can be constant or generating function
    tanlw = 0.2              # line width of tangents
    tanalpha = 0.2           # tranparency of tangents
    filename = None          # file name to save to. Defaults to date and time
    keep_partials = False    # keep partial files after render finishes
    def __init__(self, **options):
        self.set_options(**options)
    def set_options(self, **options):
        for o,v in options.items():
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
    #@timed(showargs=False)
    def drawTangents(self, tmin, tmax, n_tan):
        # function paramter values
        ts_ = numpy.linspace(tmin, tmax, n_tan, False)
        ts = misc.permute(ts_)
        # color array
        if type(self.tancol) == types.FunctionType:
            colors = self.tancol(ts)
        else:
            c_arr = colorConverter.to_rgba_array(self.tancol)
            colors = numpy.full((n_tan, 4), c_arr)
        # plot the tangents on current axis
        for t, c in zip(ts, colors):
            p = self.curve.taylorCurve(t, self.degree)
            s = numpy.linspace(t - self.tanlen, t + self.tanlen, self.tanres)
            pyplot.plot( p.x(s), p.y(s), color=c
                       , linewidth=self.tanlw, alpha=self.tanalpha)
        # plot the curve
        if self.showcurve:
            self.drawCurve()
            
    def drawCurve(self):
        # print "drawing"
        # return
        # print repr(self._drawCurve_constcolor)
        if type(self.curvecol) == types.FunctionType:
            self._drawCurve_varColor()
        else:
            self._drawCurve_constColor()
        
    def _drawCurve_constColor(self):
        # pass
        tmin, tmax = self.domain
        t = numpy.linspace(tmin, tmax, self.curveres)
        pyplot.plot(
              self.curve.x(t)
            , self.curve.y(t)
            , color = self.curvecol
            , lw = self.curvelw
            , alpha = self.curvealpha
            )
    def _drawCurve_varColor(self):
        tmin, tmax = self.domain
        t = numpy.linspace(tmin, tmax, self.curveres)
        x = self.curve.x(t)
        y = self.curve.y(t)
        coords = numpy.ndarray((self.curveres-1, 2, 2))
        coords[:,0,0] = x[:-1]
        coords[:,1,0] = x[1:]
        coords[:,0,1] = y[:-1]
        coords[:,1,1] = y[1:]
        colors = self.curvecol(t)
        # print colors
        segments = LineCollection( coords
                                 , colors = colors[:-1]
                                 , lw = self.curvelw )
        ax = pyplot.gca()
        ax.add_collection(segments)

    @misc.timed(False)
    def render(self, preview=False, scale=0.25):
        filename, figsize = self.filename, self.figsize,
        n_part, n_tan = self.n_part, self.n_tan
        tmin, tmax = self.domain
        # initialize filename
        if not type(filename) == str:
            filename = misc.generate_filename()
        # initialize preview options
        if preview:
            n_part = max(1, int(scale * n_part))    # must be int >= 1
            figsize = (scale * figsize[0], scale * figsize[1])
            n_tan = int(scale * n_tan)
            filename = "{}_preview{}".format(filename, scale)
        
        # set up the ploting surface
        fig = self.initializeFigure(figsize)
        # render partials
        dt = (tmax-tmin)/n_tan
        ds = numpy.linspace(tmin, tmin+dt, n_part, False)
        indexes = range(n_part)
        partial_filenames = []
        for i, d in zip(indexes, ds):
            self.initializeAxes()  # clear the current axes
            self.drawTangents(tmin+d, tmax+d, n_tan)
            pfname = "{}_partial{}.png".format(filename, i)
            fig.savefig(pfname, dpi = self.dpi, facecolor = self.facecolor)
            partial_filenames.append(pfname)
        # compose partials and delete partial files
        image.composeAverage(filename+".png", partial_filenames)
        if not self.keep_partials:
            for fn in partial_filenames:
                misc.deleteFile(fn)
