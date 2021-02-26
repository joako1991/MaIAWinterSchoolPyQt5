# Real-time graph plot example
This example shows how we can show in our Qt system, a graph make with the
library MatPlotLib, that evolves with the time. The time evolution is made
by the usage of a QTimer.

MatPlotLib is a very handy, useful library, that allow us to create different
type of plots, in 2D or 3D, and also to update them regularly, in order
to have an evolution of a curve.

Integrate a MatPlotLib window to the Qt system is not trivial, but since we
have a ImageWidget available from the example ShowImageExample, we can use it
to show an static plot of our curve, bar plot, or whatever we created using
matplotlib.

This example shows a cosine function, modulated by an exponential function.
The modulation function have a constant multiplying it, that changes every
100 mS, i.e., each time the QTimer timeout is reached. When this happens,
we create again the plot with the new constant value that multiplies the exponent
and we update the shown image. As a result, we have a real-time like plot,
that evolves with the time.

# Application screenshot
![app screenshot](/PyQtExamples/15_TimerAndGraphPlotsExample/images/GraphEvolutionExample.png)