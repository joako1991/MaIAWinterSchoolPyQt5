# LUT application example
This example shows how to apply a LUT to an image. The code in this example
is applied only to gray-level images, but extending this code for color images
is trivial.

We added three common LUTs:
* Increasing brightness: We increase the pixel values by 40.
* Increasing contrast: All the values between the range 50 and 200 are mapped to be
    in the range 0 - 255. The values between 0 and 50 are mapped to zero, and the ones
    in the range 200 - 255 are mapped to 255.
* Gamma correction: We create the gamma function for a given gamma value, and
    we apply the LUT to the given image to see its effect.

We plot the LUTs, and we also created the function that applies the LUT to the image
in a single step.

# Application screenshot
![app screenshot](/OpenCVExamples/08_LUTExample/images/increaseBrightness.png)
![app screenshot](/OpenCVExamples/08_LUTExample/images/increaseContrast.png)
![app screenshot](/OpenCVExamples/08_LUTExample/images/GammaCorrection.png)