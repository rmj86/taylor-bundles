import traceback
import sys

import taylorbundle as tb
import taylorbundle
import curve
import colormix
from colormix import normalize, smoothstep, cosine, gaussian
import misc

import numpy


################################################################################
## Utility functions
def verysmall(a):
    """ returns True when the values of ndarray `a` are small. """
    # used when we really want the values to be 0, but this
    # can't be guaranteed due to floating errors.
    return numpy.average(a*a) <= 1e-30

###############################################################################
## Color mixer test cases.
##
# helper function. tests that that the argument produces a 
# color function which returns [1,0,0,1] (red).
def fromConstant_helper(arg):
    colorfunc = colormix.fromConstant(arg)
    t = numpy.array([-1,0,10,10000])
    c = colorfunc(t)
    c_ = (1,0,0,1)
    b = type(c) == numpy.ndarray  and  (c==c_).all()
    return b
# colormix - fromConstant can take rgb-tuple argument
def cm_fromConstant_rgbTupleArg():
    return fromConstant_helper((1,0,0))
# colormix - fromConstant can take rgba-tuple argument
def cm_fromConstant_rgbaTupleArg():
    return fromConstant_helper((1,0,0,1))
# colormix - fromConstant can take color char argument
def cm_fromConstant_charArg():
    return fromConstant_helper('r')
# colormix - fromConstant can take color string argument
def cm_fromConstant_stringArg():
    return fromConstant_helper("red")
# colormix - fromConstant can take color hex-string argument
def cm_fromConstant_hexStringArg():
    return fromConstant_helper("#ff0000")
# colormix - fromConstant returns a color function unchanged
def cm_fromConstant_functionArg():
    colorfunc = colormix.mix2("r", "g", None)
    colorfunc2 = colormix.fromConstant(colorfunc)
    b = colorfunc is colorfunc2
    return b

# colormix._bounded tests
def cm__bounded_test1():
    t = numpy.linspace(0,1,7)
    s = numpy.linspace(0,1,7)
    colormix._bounded(t)
    b = (t==s).all()
    return b
def cm__bounded_test2():
    t = numpy.array([-1, -0.5, 0, 0.5, 1, 1.5, 2])
    s = numpy.array([ 0,    0, 0, 0.5, 1,   1, 1])
    b = (colormix._bounded(t) == s).all()
    return b

# colormix.normalize tests
def cm_normalize_test1():
    s = numpy.linspace(0,1,8)
    t = numpy.linspace(0,1,8)
    t = colormix.normalize(0,1)(t)
    b = (s==t).all()
    return b
def cm_normalize_test2():
    s = numpy.linspace(0,1,8)
    t = numpy.linspace(2,7,8)
    t = colormix.normalize(2,7)(t)
    b = verysmall(s-t)
    return b
def cm_normalize_test3():
    s = numpy.linspace(0,1,11)
    t = numpy.linspace(10,2*numpy.pi,11)
    t = colormix.normalize(10,2*numpy.pi)(t)
    b = verysmall(s-t)
    return b

# mix2 test with HTML hex color and smoothstep
def cm_mix2_hexcolor_smoothstep_normalColorMix():
    t = numpy.array([1,3,5])
    norm = colormix.smoothstep(2.,4.)
    colorfunc = colormix.mix2("#ff0000", "#0000ff", norm, linear=False)
    colors = colorfunc(t)
    colors_ = numpy.array([[ 1, 0,  0, 1]
                          ,[.5, 0, .5, 1]
                          ,[ 0, 0,  1, 1]])
    b = (colors == colors_).all()
    return b
def cm_mix2_hexcolor_smoothstep_linearColorMix():
    t = numpy.array([1,3,5])
    norm = colormix.smoothstep(2.,4.)
    colorfunc = colormix.mix2("#ff0000", "#0000ff", norm, linear=True)
    colors = colorfunc(t)
    sq2 = numpy.sqrt(2)/2
    colors_ = numpy.array([[1,   0,   0, 1]
                          ,[sq2, 0, sq2, 1]
                          ,[0,   0,   1, 1]])
    b = (colors == colors_).all()
    return b

## colormix.smoothstep - returns correct result for some obvious arguments
def cm_smoothstep_valuesInsideStepDomain():
    t = numpy.array([2,3.5,5])
    m = colormix.smoothstep(2,5)
    v = m(t)
    b = (v == [0,0.5,1]).all()
    return b
def cm_smoothstep_constOutsideStepDomain():
    t = numpy.array([0,1,2,4,5,6])
    m = colormix.smoothstep(2,4)
    v = m(t)
    b = (v == [0,0,0,1,1,1]).all()
    return b
# colormix.cosine - returns correct result for some obvious arguments
def cm_cosine_values1():
    t = numpy.arange(0,5)
    m = colormix.cosine(0,2)
    v = m(t)
    v_ = [0, 0.5, 1, 0.5, 0]
    b = verysmall(v - v_)
    return b
def cm_cosine_values2():
    t = numpy.array([-4, 0, 4, 8])
    m = colormix.cosine(0,4)
    v = m(t)
    v_ = [1, 0, 1, 0]
    b = verysmall(v - v_)
    return b
# colormix.gaussian - returns correct result for some obvious arguments
def cm_gaussian_values1():
    t = numpy.arange(0,5)
    m = colormix.gaussian(2,2)
    v = m(t)
    v_ = [.0625, .5, 1, .5, .0625]
    b = verysmall(v - v_)
    return b
def cm_gaussian_values2():
    t = numpy.array([-1,3,5,7,11])
    m = colormix.gaussian(5,4)
    v = m(t)
    v_ = [2**-9, .5, 1, .5, 2**-9]
    b = verysmall(v - v_)
    return b


################################################################################
## misc test cases
##

# permute - does not produce an array with duplicate entries
def misc_permute_nonDuplicateEntries():
    m = 100
    failed = []
    for i in range(m):
        u = numpy.arange(i)
        v = misc.permute(u)
        v.sort()
        if not numpy.all(u==v):
            return False
    return True
# permute - produces the right ordering ("fibonacci permutation")
def misc_permute_rightOrder():
    r = numpy.arange(8)
    r = misc.permute(r)
    s = numpy.array([0, 5, 2, 7, 4, 1, 6, 3])
    b = (r==s).all()
    return b

###############################################################################
##  Renderer Tests: These will signal success as long as the renderer doesn't
##  crash. The correctness of the resulting image must be inspectedf manually.
##  The image file should be given a name hinting at whant the image should
##  look like.

## draw const color curve
def tb_curveColorConst():
    bundle = tb.TaylorBundle(
          filename = "test/tb_curveColorConst"
        , curve = curve.Trochoid(-5, 0.6, 0)
        , curvelw = 10
        , curvecol = 'w'
        , showcurve = True
        , n_tan = 0
        , dpi = 30
        , window = [-4,4,-2.25,2.25]
        )
    bundle.render()
    return True

## draw variable color curve
def tb_curveColorVar():
    cm = colormix.mix2("b", "r", cosine(0, tb.tau/2), linear=True)
    bundle = tb.TaylorBundle(
          filename = "test/tb_curveColorVar"
        , curve = curve.Trochoid(-5, 0.6, 0)
        , curvelw = 10
        , curveres = 128
        , curvecol = cm
        , showcurve = True
        , n_tan = 0
        , dpi = 30
        , window = [-4,4,-2.25,2.25]
        )
    bundle.render()
    return True

# draw nothing, neither curve nor any tangents!
def tb_blankImage():
    bundle = tb.TaylorBundle(
          filename = "test/tb_blankImage"
        , curve = curve.Trochoid(-5, 0.6, 0)
        , showcurve = False
        , curvelw = 10
        , n_tan = 0
        , tanlw = 10
        , tanalpha = 1
        , dpi = 30
        , window = [-4,4,-2.25,2.25]
        )
    bundle.render()
    return True

## draw tangents in half the domain only
def tb_tangentsOnTheLeft():
    bundle = tb.TaylorBundle(
          filename = "test/tb_tangentsOnTheLeft"
        , curve = curve.Curve(lambda x: x, numpy.sin)
        , curvelw = 10
        , curvecol = 'w'
        , curvedomain = [-7,7]
        , n_tan = 100
        , tanlw = 2
        , tanalpha = 1
        , tancol = 'r'
        , bundledomain = [-7,0]
        , dpi = 30
        , window = [-8,8,-4.5,4.5]
        )
    bundle.render()
    return True
# draw tagents in full domain - test is to make sure that setting *domain*
# overrides *curvedomain* and *bundledomain*
def tb_curveAndTangentInFullDomain():
    bundle = tb.TaylorBundle(
          filename = "test/tb_curveAndTangentInFullDomain"
        , curve = curve.Curve(lambda x: x, numpy.sin)
        , curvelw = 10
        , curvecol = 'w'
        , curvedomain = [-7,-4]
        , n_tan = 100
        , tanlw = 2
        , tanalpha = 1
        , tancol = 'r'
        , bundledomain = [4,7]
        , dpi = 30
        , window = [-8,8,-4.5,4.5]
        )
    bundle.set_options(domain = [-8,8])
    bundle.render()
    return True
# draw tangents with variable alpha value - high when the sin is
# increasing, and low when it's decreasing. 
def tb_variableTanAlpha_highWhenIncreasing():
    mix = colormix.mix2([1,0,0,1], [1,0,0,0], cosine(0, numpy.pi))
    bundle = tb.TaylorBundle(
          filename = "test/tb_variableTanAlpha_highWhenIncreasing"
        , curve = curve.Curve(lambda x: x, numpy.sin)
        , curvelw = 6
        , curvecol = 'w'
        , n_tan = 100
        , tanlw = 2
        , tanalpha = None
        , tancol = mix
        , domain = [-13, 13]
        , dpi = 30
        , window = [-16,16,-9,9]
        )
    bundle.render()
    return True
# draw curve with variable alpha value - high when the sin is
# increasing, and low when it's decreasing.
def tb_variableCurveAlpha_highWhenIncreasing():
    mix = colormix.mix2([1,1,1,1], [1,1,1,0], cosine(0, numpy.pi))
    bundle = tb.TaylorBundle(
          filename = "test/tb_variableCurveAlpha_highWhenIncreasing"
        , curve = curve.Curve(lambda x: x, numpy.sin)
        , curvelw = 6
        , curvecol = mix
        , curvealpha = None
        , n_tan = 100
        , tanlw = 4
        , tanalpha = 0.25
        , domain = [-13, 13]
        , dpi = 30
        , window = [-16,16,-9,9]
        )
    bundle.render()
    return True
# tanalpha should ovveride alpha values in tancol arg (variable or not)
def tb_blankImage2():
    mix = colormix.mix2([1,0,0,1], [1,0,0,0], cosine(0, numpy.pi))
    bundle = tb.TaylorBundle(
          filename = "test/tb_blankImage2"
        , curve = curve.Curve(lambda x: x, numpy.sin)
        , showcurve = False
        , n_tan = 100
        , tancol = mix
        , tanlw = 2
        , tandomain = [-30, 30]
        , tanalpha = 0
        , domain = [-13, 13]
        , dpi = 30
        , window = [-16,16,-9,9]
        )
    bundle.render()
    return True
# curvealpha should override alpha values in (constant) curvecol arg
def tb_blankImage3():
    bundle = tb.TaylorBundle(
          filename = "test/tb_blankImage3"
        , curve = curve.Curve(lambda x: x, numpy.sin)
        , showcurve = True
        , curvecol = "w"
        , curvelw = 6
        , curvealpha = 0
        , n_tan = 0
        , domain = [-13, 13]
        , dpi = 30
        , window = [-16,16,-9,9]
        )
    bundle.render()
    return True
# curveAlpha should override alpha values in (variable) curvecol arg
def tb_blankImage4():
    mix = colormix.mix2([1,1,1,1], [1,1,1,0], cosine(0, numpy.pi))
    bundle = tb.TaylorBundle(
          filename = "test/tb_blankImage4"
        , curve = curve.Curve(lambda x: x, numpy.sin)
        , showcurve = True
        , curvecol = mix
        , curvelw = 6
        , curvealpha = 0
        , n_tan = 0
        , domain = [-13, 13]
        , dpi = 30
        , window = [-16,16,-9,9]
        )
    bundle.render()
    return True
# drawing tangents only in the positive direction
def tb_unidirectioanlTangents():
    bundle = tb.TaylorBundle(
          filename = "test/tb_unidirectioanlTangents"
        , curve = curve.Curve(lambda x: x, numpy.sin)
        , showcurve = True
        , curvelw = 6
        , n_tan = 100
        , tanlw = 4
        , tandomain = [0,4]
        , domain = [-13, 13]
        , dpi = 30
        , window = [-16,16,-9,9]
        )
    bundle.render()
    return True
    
# draw a thick colored line - normal color mixing
def cm_cosine_normalColorGradient_rgRgr():
    c = curve.fromFunction(lambda x: numpy.zeros(x.shape))
    mix = colormix.mix2("r", "g", cosine(0, 1), linear = False)
    bundle = tb.TaylorBundle(
          filename = "test/cm_cosine_normalColorGradient_rgRgr"
        , curve = c
        , curvecol = mix
        , showcurve = True
        , curvelw = 72 * 2
        , curveres = 481
        , window = [0, 4, -1, 1]
        , domain = [0, 4]
        , n_tan = 0
        , dpi = 30
        )
    bundle.render()
    return True
# draw a thick colored line - linear color mixing
def cm_cosine_linearColorGradient_rgRgr():
    c = curve.fromFunction(lambda x: numpy.zeros(x.shape))
    mix = colormix.mix2("r", "g", cosine(0, 1), linear = True)
    bundle = tb.TaylorBundle(
          filename = "test/cm_cosine_linearColorGradient_rgRgr"
        , curve = c
        , curvecol = mix
        , showcurve = True
        , curvelw = 72 * 2
        , curveres = 481
        , window = [0, 4, -1, 1]
        , domain = [0, 4]
        , n_tan = 0
        , dpi = 30
        )
    bundle.render()
    return True
# color mixing can take another mixer as argument
def cm_cosine_threeColorGradient_rybyRybyr():
    c = curve.fromFunction(lambda x: numpy.zeros(x.shape))
    mix1 = colormix.mix2("r", "b",     cosine(0, 1))
    mix2 = colormix.mix2(mix1, "gold", cosine(0, 0.5))
    bundle = tb.TaylorBundle(
          filename = "test/cm_cosine_threeColorGradient_rybyRybyr"
        , curve = c
        , curvecol = mix2
        , showcurve = True
        , curvelw = 72 * 2
        , curveres = 481
        , window = [-0, 4, -1, 1]
        , domain = [-0, 4]
        , n_tan = 0
        , dpi = 30
        )
    bundle.render()
    return True

# gaussin colormix base cases
def cm_gaussian_redWithBluePeakLinear():
    c = curve.fromFunction(lambda x: numpy.zeros(x.shape))
    mix = colormix.mix2("red", "dodgerBlue", gaussian(0.5, 0.1), linear=True)
    bundle = tb.TaylorBundle(
          filename = "test/cm_gaussian_redWithBluePeakLinear"
        , curve = c
        , curvecol = mix
        , showcurve = True
        , curvelw = 72 * 2
        , curveres = 481
        , window = [0, 1, -1, 1]
        , domain = [0, 1]
        , n_tan = 0
        , dpi = 30
        )
    bundle.render()
    return True
def cm_gaussian_redWithBluePeakNormal():
    c = curve.fromFunction(lambda x: numpy.zeros(x.shape))
    mix = colormix.mix2("red", "dodgerBlue", gaussian(0.5, 0.1), linear=False)
    bundle = tb.TaylorBundle(
          filename = "test/cm_gaussian_redWithBluePeakNormal"
        , curve = c
        , curvecol = mix
        , showcurve = True
        , curvelw = 72 * 2
        , curveres = 481
        , window = [0, 1, -1, 1]
        , domain = [0, 1]
        , n_tan = 0
        , dpi = 30
        )
    bundle.render()
    return True

# gaussian can take another mixer as color arg,
def cm_gaussian_redWithPeaksLeftWideRightThin():
    c = curve.fromFunction(lambda x: numpy.zeros(x.shape))
    mix1 = colormix.mix2("red", "dodgerBlue", gaussian(-0.5, 0.4))
    mix2 = colormix.mix2(mix1,  "dodgerblue", gaussian( 0.5, 0.1))
    bundle = tb.TaylorBundle(
          filename = "test/cm_gaussian_redWithPeaksLeftWideRightThin"
        , curve = c
        , curvecol = mix2
        , showcurve = True
        , curvelw = 72 * 2
        , curveres = 481
        , window = [-1, 1, -1, 1]
        , domain = [-1, 1]
        , n_tan = 0
        , dpi = 30
        )
    bundle.render()
    return True

# normalize / "sharpstep" basic case
def cm_normalize_redToBlue():
    c = curve.fromFunction(lambda x: numpy.zeros(x.shape))
    mix = colormix.mix2("red", "blue", normalize(1, 2))
    bundle = tb.TaylorBundle(
          filename = "test/cm_normalize_redToBlue"
        , curve = c
        , curvecol = mix
        , showcurve = True
        , curvelw = 72 * 2
        , curveres = 481
        , window = [0, 3, -1, 1]
        , domain = [0, 3]
        , n_tan = 0
        , dpi = 30
        )
    bundle.render()
    return True

# smoothstep basic case
def cm_smoothstep_redToBlue():
    c = curve.fromFunction(lambda x: numpy.zeros(x.shape))
    mix = colormix.mix2("red", "blue", smoothstep(1, 2))
    bundle = tb.TaylorBundle(
          filename = "test/cm_smoothstep_redToBlue"
        , curve = c
        , curvecol = mix
        , showcurve = True
        , curvelw = 72 * 2
        , curveres = 481
        , window = [0, 3, -1, 1]
        , domain = [0, 3]
        , n_tan = 0
        , dpi = 30
        )
    bundle.render()
    return True
# smoothstep can take another mixer as argument
def cm_smoothstep_redToGreenToBlue():
    c = curve.fromFunction(lambda x: numpy.zeros(x.shape))
    mix1 = colormix.mix2("red", "green", smoothstep(2, 3))
    mix2 = colormix.mix2(mix1,  "blue",  smoothstep(6, 7))
    bundle = tb.TaylorBundle(
          filename = "test/cm_smoothstep_redToGreenToBlue"
        , curve = c
        , curvecol = mix2
        , showcurve = True
        , curvelw = 72 * 2
        , curveres = 481
        , window = [0, 9, -1, 1]
        , domain = [0, 9]
        , n_tan = 0
        , dpi = 30
        )
    bundle.render()
    return True

# taylorbundle can use matplotlib colormaps
def cm__matplotlibColormapViridisGradient():
    import matplotlib
    c = curve.fromFunction(lambda x: numpy.zeros(x.shape))
    colors = colormix.colormap("viridis", colormix.normalize(0,9))
    bundle = tb.TaylorBundle(
          filename = "test/cm__matplotlibColormapViridisGradient"
        , curve = c
        , curvecol = colors
        , showcurve = True
        , curvelw = 72 * 2
        , curveres = 481
        , window = [0, 9, -1, 1]
        , domain = [0, 9]
        , n_tan = 0
        , dpi = 30
        )
    bundle.render()
    return True
    
# the color maps work even when the normalization is out of bounds
def cm_oob_wideRedBand():
    c = curve.fromFunction(lambda x: numpy.zeros(x.shape))
    norm = lambda t: 8 * gaussian(0.5, 0.3)(t) - 4
    colorfunc = colormix.mix2((0.2,0,0.2), 'r', norm)
    bundle = tb.TaylorBundle(
          filename = "test/cm_oob_wideRedBand"
        , curve = c
        , curvecol = colorfunc
        , showcurve = True
        , curvelw = 72 * 2
        , curveres = 481
        , window = [0, 1, -1, 1]
        , domain = [0, 1]
        , n_tan = 0
        , dpi = 30
        )
    bundle.render()
    return True
def cm_oob_wideViridisBand():
    c = curve.fromFunction(lambda x: numpy.zeros(x.shape))
    norm = lambda t: 8 * gaussian(0.5, 0.3)(t) - 4
    colorfunc = colormix.colormap("viridis", norm)
    bundle = tb.TaylorBundle(
          filename = "test/cm_oob_wideViridisBand"
        , curve = c
        , curvecol = colorfunc
        , showcurve = True
        , curvelw = 72 * 2
        , curveres = 481
        , window = [0, 1, -1, 1]
        , domain = [0, 1]
        , n_tan = 0
        , dpi = 30
        )
    bundle.render()
    return True

# TODO: what happens when n_parts is 0?

###############################################################################
## TB option setter

# setting options at init
def t_TaylorBundle_optionSetter_1():
    tb = taylorbundle.TaylorBundle(n_tan = 12345, n_part = 77)
    b = tb.n_tan == 12345 and tb.n_part == 77
    return b
# setting options with method set_options
def t_TaylorBundle_optionSetter_2():
    tb = taylorbundle.TaylorBundle()
    tb.set_options(n_tan = 12345, n_part = 77)
    b = tb.n_tan == 12345 and tb.n_part == 77
    return b
# setting options with direct attr access
def t_TaylorBundle_optionSetter_3():
    tb = taylorbundle.TaylorBundle()
    tb.n_tan = 12345
    tb.n_part = 77
    b = tb.n_tan == 12345 and tb.n_part == 77
    return b
# setting 'domain' in init
def t_TaylorBundle_optionSetter_4():
    tb = taylorbundle.TaylorBundle(domain = [2,77])
    b = tb.bundledomain == [2,77] and tb.curvedomain == [2,77]
    return b
# setting 'domain' with set_options
def t_TaylorBundle_optionSetter_5():
    tb = taylorbundle.TaylorBundle()
    tb.set_options(domain = [2,77])
    b = tb.bundledomain == [2,77] and tb.curvedomain == [2,77]
    return b
# setting 'domain' with direct attr access
def t_TaylorBundle_optionSetter_6():
    tb = taylorbundle.TaylorBundle()
    tb.domain = [2,77]
    b = tb.bundledomain == [2,77] and tb.curvedomain == [2,77]
    return b
# can not set an arbitrary attribute - only attributes the object already has
# at init
def t_TaylorBundle_optionSetter_7():
    try:
        tb = taylorbundle.TaylorBundle(hotDogsWithKetchup = "every single day")
    except AttributeError:
        return True
    return False
# can not set arbitrary attributes - with set_options
def t_TaylorBundle_optionSetter_8():
    tb = taylorbundle.TaylorBundle()
    try:
        tb.set_options( hotDogsWithKetchup = "every single day" )
    except AttributeError:
        return True
    return False
# can not set arbitrary attributes - with direct access
def t_TaylorBundle_optionSetter_9():
    tb = taylorbundle.TaylorBundle()
    try:
        tb.hotDogsWithKetchup = "every single day"
    except AttributeError:
        return True
    return False

###############################################################################
## test running infrastructure

def runtest(f, v=3):
    """ run test function. *f* should take no arguments and returns a Bool.
        Verbosity levels:
            0 -> print nothing
            1 -> print if the function throws an error
            2 -> print the error call stack (only at this level)
            3 -> print if the function returns false
            4 -> print if the function succeeds."""
    f_name = f.__name__
    try:
        b = f()
    except Exception as e:
        if v == 2:
            traceback.print_exc(e)
        elif v >= 1:
            print "Exception in {}: {}".format(f_name, repr(e))
    else:
        if b and v >= 4:
            print "{} succeeded".format(f_name)
        elif not b and v >= 2:
            print "{} FAILED!!!".format(f_name)

def testAll(fs, v=3):
    for f in fs:
        runtest(f, v=v)

def cm_tests(v=3):
    testAll( [ cm_fromConstant_rgbTupleArg
             , cm_fromConstant_rgbaTupleArg
             , cm_fromConstant_charArg
             , cm_fromConstant_stringArg
             , cm_fromConstant_hexStringArg
             , cm_fromConstant_functionArg
             , cm__bounded_test1
             , cm__bounded_test2
             , cm_normalize_test1
             , cm_normalize_test2
             , cm_normalize_test3
             , cm_mix2_hexcolor_smoothstep_normalColorMix
             , cm_mix2_hexcolor_smoothstep_linearColorMix
             , cm_smoothstep_valuesInsideStepDomain
             , cm_smoothstep_constOutsideStepDomain
             , cm_cosine_values1
             , cm_cosine_values2
             , cm_gaussian_values1
             , cm_gaussian_values2
             ]
           , v = v
           )

def misc_tests(v=3):
    testAll( [ misc_permute_nonDuplicateEntries
             , misc_permute_rightOrder
             ]
           , v = v
           )

def cm_render_tests(v=3):
    testAll( [ 
               cm_normalize_redToBlue
             , cm_cosine_normalColorGradient_rgRgr
             , cm_cosine_linearColorGradient_rgRgr
             , cm_cosine_threeColorGradient_rybyRybyr
             , cm_gaussian_redWithBluePeakLinear
             , cm_gaussian_redWithBluePeakNormal
             , cm_gaussian_redWithPeaksLeftWideRightThin
             , cm_smoothstep_redToBlue
             , cm_smoothstep_redToGreenToBlue
             , cm__matplotlibColormapViridisGradient
             , cm_oob_wideRedBand
             , cm_oob_wideViridisBand
             ]
           , v = v
           )

def tb_render_tests(v=3):
    testAll( [ tb_curveColorConst
             , tb_curveColorVar
             , tb_blankImage
             , tb_blankImage2
             , tb_blankImage3
             , tb_blankImage4
             , tb_tangentsOnTheLeft
             , tb_curveAndTangentInFullDomain
             , tb_variableTanAlpha_highWhenIncreasing
             , tb_variableCurveAlpha_highWhenIncreasing
             , tb_unidirectioanlTangents
             ]
           , v = v
           )

def tb_tests(v=3):
    testAll( [ t_TaylorBundle_optionSetter_1
             , t_TaylorBundle_optionSetter_2
             , t_TaylorBundle_optionSetter_3
             , t_TaylorBundle_optionSetter_4
             , t_TaylorBundle_optionSetter_5
             , t_TaylorBundle_optionSetter_6
             , t_TaylorBundle_optionSetter_7
             , t_TaylorBundle_optionSetter_8
             , t_TaylorBundle_optionSetter_9
             ]
           , v = v
           )

if __name__ == "__main__":
    v = 3
    if len(sys.argv) >= 2:
        useDefault = False
        # get verbosity level
        try:
            s = sys.argv[1]
            n = int(s)
        except:
            useDefault = True
        else:
            if n<0 or n>4:
                useDefault = True
        if useDefault:
            print "verbosity should be an int between 0 and 4. got: " + s
            print "Using default value: {}".format(v)
        else:
            v = n

    tb_tests(v=v)
    cm_tests(v=v)
    misc_tests(v=v)
    cm_render_tests(v=v)
    tb_render_tests(v=v)