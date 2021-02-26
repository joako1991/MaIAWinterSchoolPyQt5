# Histogram equalization example
This example covers the histogram equalization operation. It shows two cases:
Histogram equalization of the RGB image, per channel, and the histogram equalization
in HSV, changing the value channel.

In both cases, the original image and the output image are shown.

The created functions are the most generic we can think of: if we provide the right
data, the functions work always. The example functions only receive the filepath
of the image to be opened. The function that computes the histogram accepts images
coded in any amount of bits, the function that computes the APF has not any
problem regarding the image size, and the histogram equalization function
works for both, gray-level and color images.

# Application screenshot
![app screenshot](/OpenCVExamples/14_HistogramEqualizationExample/images/HSVEqualization.png)
![app screenshot](/OpenCVExamples/14_HistogramEqualizationExample/images/RGBEqualization.png)
