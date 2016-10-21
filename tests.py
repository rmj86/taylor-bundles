import traceback
import sys

import taylorbundle as tb
import curve
import colormix
import misc

import numpy


###############################################################################
## Color mixer test cases.

## colormix - can take rgb tuple as color value
def cm_cos2_3tupleCol():
    cmix = colormix.cosine2((1,0,0),(0,0,1),0,1)
    t = numpy.array([0.5])
    c = cmix(t)
    b = (c == (0.5, 0, 0.5, 1)).all()
    return b
## colormix - can take rgba colors
def cm_cos2_4tupleCol():
    cmix = colormix.cosine2((1,0,0,0), (0,0,1,1), 0, 1)
    t = numpy.array([0.5])
    c = cmix(t)
    b = (c == (0.5, 0, 0.5, 0.5)).all()
    return b
## colormix - can take matplotlib color char as color value
def cm_cos2_charCol():
    cmix = colormix.cosine2('r', 'b', 0, 1)
    t = numpy.array([0.5])
    c = cmix(t)
    b = (c == (0.5, 0, 0.5, 1)).all()
    return b
## colormix - can take matplotlib color string as color value
def cm_cos2_strCol():
    cmix = colormix.cosine2('red', 'blue', 0, 1)
    t = numpy.array([0.5])
    c = cmix(t)
    b = (c == (0.5, 0, 0.5, 1)).all()
    return b
## colormix - can take hex string color aruments
def cm_cos2_hexCol():
    cmix = colormix.cosine2('#ff0000', '#0000ff', 0, 1)
    t = numpy.array([0.5])
    c = cmix(t)
    b = (c == (0.5, 0, 0.5, 1)).all()
    return b
## colormix - can take mixed color values
def cm_cos2_mixedCol():
    cmix = colormix.cosine2('r', (0,0,1), 0, 1)
    t = numpy.array([0.5])
    c = cmix(t)
    b = (c == (0.5, 0, 0.5, 1)).all()
    return b
## colormix - can take numpy arr as parameter value
def cm_cos2_arrParam():
    cmix = colormix.cosine2((1,0,0,0), (0,0,1,1), 0, 1)
    t = cmix(numpy.linspace(0,1,3))
    t2 = numpy.ndarray((3,4))
    t2[0] = (1, 0, 0, 0)
    t2[1] = (0.5, 0, 0.5, 0.5)
    t2[2] = (0, 0, 1, 1)
    b = (t == t2).all()
    return b
## colormix - can take arr parameter and different colors when linear=True
def cm_cos2_arrParamLinear():
    cmix = colormix.cosine2((1,0,0,0), (0,0,1,1), 0, 1, linear=True)
    t = cmix(numpy.linspace(0,1,3))
    t2 = numpy.ndarray((3,4))
    sqt2 = numpy.sqrt(2)/2
    t2[0] = (1, 0, 0, 0)
    t2[1] = (sqt2, 0, sqt2, sqt2)
    t2[2] = (0, 0, 1, 1)
    b = (t == t2).all()
    return b

####################
## misc test cases

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
        , n_tan = 1
        , dpi = 30
        , window = [-4,4,-2.25,2.25]
        )
    bundle.render()
    return True

## draw variable color curve
def tb_curveColorVar():
    cm = colormix.cosine2((1,0,0),(0,1,0),0,tb.tau/10)
    t = numpy.linspace(0,1,3)
    bundle = tb.TaylorBundle(
          filename = "test/tb_curveColorVar"
        , curve = curve.Trochoid(-5, 0.6, 0)
        , curvelw = 10
        , curveres = 128
        , curvecol = colormix.cosine2((1,0,0),(0,1,0),0,tb.tau/10, linear=True)
        , showcurve = True
        , n_tan = 1
        , tanalpha = 0
        , dpi = 30
        , window = [-4,4,-2.25,2.25]
        )
    bundle.render()
    return True

# draw nothing, neither curve nor any tangents!
def tb_blankImage():
    cm = colormix.cosine2((1,0,0),(0,1,0),0,tb.tau/10)
    t = numpy.linspace(0,1,3)
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
    t = numpy.linspace(0,1,3)
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
    t = numpy.linspace(0,1,3)
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

# draw a thick colored line - normal color mixing
def cm_cos2_normalColorGradient():
    c = curve.fromFunction(lambda x: numpy.zeros(x.shape))
    mix = colormix.cosine2("r", "g", -1, 1, linear = False)
    bundle = tb.TaylorBundle(
          filename = "test/cm_cos2_normalColorGradient"
        , curve = c
        , curvecol = mix
        , showcurve = True
        , curvelw = 10*30
        , curveres = 100
        , window = [-1.1, 1.1, -1, 1]
        , domain = [-1, 1]
        , n_tan = 0
        , dpi = 30
        )
    bundle.render()
    return True
# draw a thick colored line - linear color mixing
def cm_cos2_linearColorGradient():
    c = curve.fromFunction(lambda x: numpy.zeros(x.shape))
    mix = colormix.cosine2("r", "g", -1, 1, linear = True)
    bundle = tb.TaylorBundle(
          filename = "test/cm_cos2_linearColorGradient"
        , curve = c
        , curvecol = mix
        , showcurve = True
        , curvelw = 10*30
        , curveres = 100
        , window = [-1.1, 1.1, -1, 1]
        , domain = [-1, 1]
        , n_tan = 0
        , dpi = 30
        )
    bundle.render()
    return True
# color mixing can take another mixer as argument
def cm_cos2_threeColorGradient():
    c = curve.fromFunction(lambda x: numpy.zeros(x.shape))
    mix1 = colormix.cosine2("r", "b", -1, 1)
    mix2 = colormix.cosine2("g", mix1, 0, 1)
    bundle = tb.TaylorBundle(
          filename = "test/cm_cos2_threeColorGradient"
        , curve = c
        , curvecol = mix2
        , showcurve = True
        , curvelw = 10*30
        , curveres = 100
        , window = [-1.1, 1.1, -1, 1]
        , domain = [-1, 1]
        , n_tan = 0
        , dpi = 30
        )
    bundle.render()
    return True


# TODO: what happens when n_parts is 0?


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
        elif not b and v >= 3:
            print "{} FAILED!!!".format(f_name)

def testAll(fs, v=3):
    for f in fs:
        runtest(f, v=v)

def cm_tests(v=3):
    testAll( [ cm_cos2_3tupleCol
             , cm_cos2_4tupleCol
             , cm_cos2_charCol
             , cm_cos2_strCol
             , cm_cos2_hexCol
             , cm_cos2_mixedCol
             , cm_cos2_arrParam
             , cm_cos2_arrParamLinear
             ]
           , v = v
           )
def misc_tests(v=3):
    testAll( [ misc_permute_nonDuplicateEntries
             , misc_permute_rightOrder
             ]
           , v = v
           )

def render_tests(v=3):
    testAll( [ tb_curveColorConst
             , tb_curveColorVar
             , tb_blankImage
             , tb_tangentsOnTheLeft
             , tb_curveAndTangentInFullDomain
             , cm_cos2_normalColorGradient
             , cm_cos2_linearColorGradient
             , cm_cos2_threeColorGradient
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

    render_tests(v=v)
    cm_tests(v=v)
    misc_tests(v=v)
