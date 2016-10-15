import traceback
import sys

import taylorbundle as tb
import curve
import colormix

import numpy



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


## draw const color curve
def tb_curveColorConst():
    bundle = tb.TaylorBundle(
          filename = "test/tb_curveColorConst"
        , curve = curve.Trochoid(-5, 0.6, 0)
        , curvelw = 10
        , curvecol = 'w'
        , n_tan = 1
        , dpi = 30
        , window = [-4,4,-2.25,2.25]
        )
    bundle.render()


## draw variable color curve
def tb_curveColorVar():
    cm = colormix.cosine2((1,0,0),(0,1,0),0,tb.tau/10)
    t = numpy.linspace(0,1,3)
    print t
    print cm(t)
    # print cm(1)
    bundle = tb.TaylorBundle(
          filename = "test/tb_curveColorVar"
        , curve = curve.Trochoid(-5, 0.6, 0)
        , curvelw = 10
        , curvecol = colormix.cosine2((1,0,0),(0,1,0),0,tb.tau/10)
        , n_tan = 1
        , dpi = 30
        , window = [-4,4,-2.25,2.25]
        )
    # bundle.render()



## test different curve- and bundle domains
## TODO

## test having 0 n_tans
## TODO

def renderTests():
    tb_curveColorConst()
    tb_curveColorVar()

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
    
    # renderTests()
    cm_tests(v=v)
