# Load and show color image channel example
In this example we extend the application of the example 01_ShowImageExample.
Now, besides opening and showing a color image, we show its channels separatedly.
These images are gray-level images. If we want to show them as color (only
red, only green and only blue) we have to create an empty image and put the red
matrix only in the red channel of the empty image, create another empty image
and put only the green channel on it, and do the same for the blue.

Since they are gray-level images, the darker the pixel value, the less of that
color we have in that pixel, and the more white the pixel, the more of that
color we have in the pixel.

# Application screenshot
![app screenshot](/OpenCVExamples/02_ShowChannelsExample/images/SeparatedChannels.png)