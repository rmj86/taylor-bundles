Short term:

1. ~~Add the program and module files.~~
2. ~~Check that they work!~~
6. ~~Add: ability to render multi-coloured generating curve~~
7. ~~Add: distinct domains for the curve and it's bundle~~
8. ~~colormix should work on numpy arrays~~
12. ~~__curve__ module should have a _fromFunction_ which take an argument f and returns a Curve(x, f(x))~~
10. ~~renderer should issue a WARNING when it is passed an invalid option.~~
3. Make a gallery of example renders
4. Write readme - how to use 
5. Comment the modules regarding implementation details
9. tangents should be able to get their (variable) alpha value from the color(-mixer) as part of the rgba tuple. If parameter _tanalpha_ is not None, it should overide the rgba alpha value

Long term:

1. Optimize rendering with pyplot.collections
2. Make a RELEASE
11. renderer should take verbosity argument - for printing render times, file saves, etc.
3. Write extension for specification and renering of animations
4. Make GUI
