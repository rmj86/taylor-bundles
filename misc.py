# -*- coding: utf-8 -*-
"""
Created on Wed Feb 17 17:37:21 2016

@author: hannes
"""

import time
import numpy
import os
import traceback

def timed(showargs=True):
    if showargs: timedstr = "executed {}(*{}, **{}) in {t}s"
    else: timedstr = "executed {}(...) in {t}s"
    def _timed(f):
        def _timed_func(*args, **kwargs):
            t0 = time.time()
            v = f(*args, **kwargs)
            t1 = time.time()
            print timedstr.format(f.__name__, args, kwargs, t=t1-t0)
            return v
        return _timed_func
    return _timed

def generate_filename():
    filename = time.strftime("taylorbundle_render_%Y-%m-%d_%H-%M-%S")
    return filename

def deleteFile(fname):
    try: os.remove(fname)
    except:
        traceback.print_stack()
        traceback.print_exc()
        print "failed to delte " + fname

###########################
#### Array Permutation ####
###########################

def permute(array):
    permut_index = fibpermut(len(array))
    return array[permut_index]

def linmod(n, i):    #
    a = (numpy.arange(n) * i) % n
    return a

def fibpermut(n):
    a, b = 1, 1
    while a < n:
        a, b = a+b, a
    p = linmod(a, b)
    q = p[p<n]
    return q
