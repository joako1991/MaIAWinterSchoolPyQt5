# Load image and compute its histogram example
In this example we show how to load an image, and to compute its histogram.
The histogram computation works only for gray-level images, but it is easily
expandable to color images.

In this example, two implementation are provided
    *) By definition: We cover all the image, pixel by pixel, and we check each
        pixel value. Then we have a counter array, with as many elements
        as possible gray-levels in the image. This array is initialized
        to zero at each position. Then, at each pixel, we add one to the histogram array
        in the position corresponding to the pixel gray-level value.

    *) Using pre-defined functions: We use the histogram function defined in Numpy
        to accomplish the same objective.

In this example program, we check the time each function takes: by definition
it takes 0,144 sec = 144 mS, and using the numpy function, it takes 0.00696 sec = 6,7 mS.
Which means our definition implementation takes 2150% more time than the NumPy
implementation. If we implement an algorithm that have to run quickly, and it
is based on computing the histogram, definitely the numpy function have to be
used.

# Application screenshot
![app screenshot](/OpenCVExamples/06_HistogramExample/images/histogramExample.png)