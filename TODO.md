Short term:

1. ~~Add the program and module files.~~
2. ~~Check that they work!~~
3. Make a gallery of example renders
4. Write readme - how to use 
5. Comment the modules regarding implementation details
6. ~~Add: ability to render multi-coloured generating curve~~
7. Add: distinct domains for the curve and it's bundle
8. ~~colormix should work on numpy arrays~~
9. remove the _alpha_ TB option - alpha should be passed as part of the color argument (rgba)
10. renderer should issue a WARNING when it is passed an invalid option.
11. renderer should take verbosity argument - for printing render times, file saves, etc.
12. __curve__ mnodule should have a _Function_ class which take an argument f(x) and returns a Curve(x, f(x))

Long term:

1. Optimize rendering with pyplot.collections
2. Make a RELEASE
3. Write extension for specification and renering of animations
4. Make GUI
