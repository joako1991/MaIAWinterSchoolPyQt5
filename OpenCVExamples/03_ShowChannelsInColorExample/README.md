# Load and show color image channel example
In this example we extend the application of the example 02_ShowChannelsExample.
Now, besides opening and showing a color image, we show its channels separatedly,
but each channel is now in color. This means: if we have a lot of red, we will
see it as an extremely intense red, and the less we have of that color, the darker
the pixel will be.

This is just a manipulation to have a better idea of what a color image is,
and what each channel represents, but the correct information is the one
shown in the example 02: the sensor only measures the intensity of the light
received, so the matrix it gives us is a gray-level image. The idea of color
is based on the knowledge we have that each pixel is overlapped with a color filter,
but from the sensor point of view, it only measures the intensity of light received
on its sensitive surface.

# Application screenshot
![app screenshot](/OpenCVExamples/03_ShowChannelsInColorExample/images/SeparatedChannels.png)