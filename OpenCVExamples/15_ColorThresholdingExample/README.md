# Color thresholding example
This example shows how we can filter an image, based on the color of the pixels.
For doing so, we use the HSV system. The color information is mainly present in
the HUE channel, so specifying the minimum and maximum hue value is enough
in order to filter.

Then, since this method will create a lot of noise in the image, we apply
some morphological operators in order to filter the image. Finally, we
multiply, element-wise, the mask and the input image, in order to know
which color we are filtering with our range of HUE.

# Application screenshot
![app screenshot](/OpenCVExamples/15_ColorThresholdingExample/images/FirstCapture.png)
![app screenshot](/OpenCVExamples/15_ColorThresholdingExample/images/SecondCapture.png)