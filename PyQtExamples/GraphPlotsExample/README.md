# Graph plot example
This example shows how we can show in our Qt system, a graph make with the
library MatPlotLib.

MatPlotLib is a very handy, useful library, that allow us to create different
type of plots, in 2D or 3D, and also to update them regularly, in order
to have an evolution of a curve.

Integrate a MatPlotLib window to the Qt system is not trivial, but since we
have a ImageWidget available from the example ShowImageExample, we can use it
to show an static plot of our curve, bar plot, or whatever we created using
matplotlib.

This example shows two static graphs make with MatPlotLib, and then converted
into OpenCV images, in order to show them. This example can be useful to represent
Histograms, or LUT functions.

# Application screenshot
![app screenshot](/PyQtExamples/GraphPlotsExample/images/GraphPlotsExample.png)