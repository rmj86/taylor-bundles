Short term:

1. ~~Add the program and module files.~~
2. ~~Check that they work!~~
6. ~~Add: ability to render multi-coloured generating curve~~
7. ~~Add: distinct domains for the curve and it's bundle~~
8. ~~colormix should work on numpy arrays~~
12. ~~__curve__ module should have a _fromFunction_ which take an argument f and returns a Curve(x, f(x))~~
10. ~~renderer should issue a WARNING when it is passed an invalid option.~~
13. ~~let a colormixer maker take another mixer as an argument, for more complex color possibilities.~~
9. ~~tangents should be able to get their (variable) alpha value from the color(-mixer) as part of the rgba tuple. If parameter _tanalpha_ is not None, it should overide the rgba alpha value~~
1. ~~Make "smoothstep" color mixer~~
1. ~~Give Curve the __add__ method, so that curves can be defined as sums of other curves.~~
1. ~~Make primitive curves Circle, Line ande Point. This allows us to define many curves, including trochoids, as sums of simple curves.~~
1. ~~colorfunctions based on matplotlib color ranges~~
4. Write readme - how to use 
    1. Index
    2. ~~Statement of purpose~~
        * ~~explain tangent lines and bundles~~
        * ~~explain taylor polynomials and bundles~~
        * ~~extend to parametric curves~~
        * ~~illustrate adding color~~
    3. ~~How to install, dependencies~~
    4. ~~How to use:~~
        * ~~example files and renders~~
        * options
    4. Other modules
        * primitive curves
        * predefined curves
        * curves, how to define your own
        * colormixer, how it works
        * colormixer, predefined options,
        * how to define your own, with examples
        * something about linear color space?
3. Make a gallery of example renders
5. Comment the modules regarding implementation details

Long term:

1. Optimize rendering with pyplot.collections
2. Make a RELEASE
11. renderer should take verbosity argument - for printing render times, file saves, etc.
12. improved rendering of colored generating curve - get rid of gaps
3. Write extension for specification and rendering of animations
4. Make GUI
