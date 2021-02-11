# Load and and convert it into HSV color space example
In this case, we take a color image, and we use the function cvtColor in order
to switch the color space from BGR to HSV. We show both images in order to compare.
It is expected that the HSV image will be wrong, since the imshow function
expects to receive a BGR image, i.e., it expects that the first channel will
correspond to the amount of blue in the image, the second one to green, and the
third one to correspond to the amount of red at each pixel. Even though the images
have a correspondance between these spaces, we cannot show them using this function
as in the original image, since the first channel corresponds to the amount of
HUE, and not to the amount of blue, the second channel corresponds to the saturation
and not to the green, and the third channel corresponds to the value, and not
to the amount of red in the image.

IMPORTANT: In OpenCV:
    *) HUE range is [0,179],
    *) Saturation range is [0,255],
    *) Value range is [0,255]

We have to consider this when we do operations in this color space. In the theory,
we said that:
    *) Hue is in the range [0, 360]
    *) Saturation is in the range [0, 100]
    *) Value is in the range [0, 100]
The solution is to normalize all the ranges to be in  [0,1], which means
that we will have to work with float values.

# Application screenshot
![app screenshot](/OpenCVExamples/04_ConvertToHSVExample/images/imshowExample.png)