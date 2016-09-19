# -*- coding: utf-8 -*-
"""
Created on Wed Feb 17 17:37:21 2016

@author: hannes
"""

import time
import numpy
import os
import traceback


# Todo:
# better permute
# analyse permutation; find linear subranges; visualise

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
    
def gcd(a,b):
    if a*b == 0:
        raise ValueError("gcd({},{}); Division by zero".format(a,b))
    while b != 0:
        a, b = b, a%b
    return a
    
def closeints(f):
    """Generates all integers, sorted according to distance from f."""
    g = round(f)
    if f < g:  # we rounded up
        j = int(g)
        i = j-1
        yield j
        j = j+1
    else:  # we rounded down
        i = int(g)
        j = i+1
    while True:
        yield i
        yield j
        i, j = i-1, j+1
    
def closerelprimes(n, f):
    """Generator of numbers relatively prime to n,
     sorted according to distance from f."""
    for i in closeints(f):
        if gcd(n,i) == 1:
            yield i
    
def linmod(n, i):    # 
    a = (numpy.arange(n) * i) % n
    return a
    
phi = 0.5*(1+5**0.5)

def fib_i(n): # increment for pseudofibpermut
    i = int(round(n/phi))
    i = closerelprimes(n, i).next()
    return i
    
def pseudofibpermut(n):
    i = fib_i(n)
    a = linmod(n, i)
    return a

def fibpermut(n):
    a, b = 1, 1
    while a < n:
        a, b = a+b, a
    p = linmod(a, b)
    q = p[p<n]
    return q
    
@timed()
def test_permute(m):
    """ test that permute(array) doesn't produce an array with duplicates."""
    failed = []
    for i in range(m):
        u = numpy.arange(i)
        v = permute(u)
        v.sort()
        if not numpy.all(u==v):
            failed.append(i)
    ts = "Finished {} tests of permute(...).\n  {} failed.\n  Failed for {}"
    print ts.format(m, len(failed), failed)

if __name__ == "__main__":
    print generate_filename()
    a = numpy.arange(8)
    b = permute(a)
    test_permute(1000)