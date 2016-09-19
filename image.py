# -*- coding: utf-8 -*-
"""
Created on Mon Feb 15 17:44:02 2016

@author: hannes
"""

# import PIL
import matplotlib
import numpy
from misc import timed

#@timed(showargs=False)
def composeAverage(fname_out, fnames_in):
    # load images and average them up
    arr0 = matplotlib.pyplot.imread(fnames_in[0])
    imgarrs = (matplotlib.pyplot.imread(fn) for fn in fnames_in[1:])
    for i in imgarrs:
        arr0 += i
    arr0 /= len(fnames_in)
    # convert to int array
    matplotlib.image.imsave(fname_out, arr0)
    # intarr = numpy.rint(arr0*255.0).astype(numpy.uint8)
    # convert to PIL.Image and save. (matplotlib.image.imsave is broken)
    # img = PIL.Image.fromarray(intarr)
    # img.save(fname_out)

def analyse(fname):
    # read the data
    rgb = matplotlib.image.imread(fname)
    hsv = matplotlib.colors.rgb_to_hsv(rgb[:,:,:3])
#    return hsv
    # set up the axes
    f, axes = matplotlib.pyplot.subplots(2,3, sharex=True, sharey=True)
    # label and plot the channels
    bins = 32
    axes[0,0].set_title("Red")
    axes[0,1].set_title("Green")
    axes[0,2].set_title("Blue")
    axes[1,0].set_title("Hue")
    axes[1,1].set_title("Saturation")
    axes[1,2].set_title("Value")
    axes[0,0].hist(rgb[:,:,0].flatten(), bins, range=[0,1], log=True, color='r')
    axes[0,1].hist(rgb[:,:,1].flatten(), bins, range=[0,1], log=True, color='g')
    axes[0,2].hist(rgb[:,:,2].flatten(), bins, range=[0,1], log=True, color='b')
    axes[1,0].hist(hsv[:,:,0].flatten(), bins, range=[0,1], log=True, color='k')
    axes[1,1].hist(hsv[:,:,1].flatten(), bins, range=[0,1], log=True, color='k')
    axes[1,2].hist(hsv[:,:,2].flatten(), bins, range=[0,1], log=True, color='k')
    # save and return
    matplotlib.pyplot.savefig("analysis_"+fname)


@timed(False)
def compose_test():
    fnames = [ "m{}test_partial{}.png".format(i,j) 
               for i in range(4) 
               for j in range(16) ]
    outname = "asdf2.png"
    composeAverage2(outname, fnames)

@timed()
def main():
    for i in range(16):
        compose_test()

if __name__ == "__main__":    
    main()
    