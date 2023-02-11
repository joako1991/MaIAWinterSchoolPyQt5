# Filtering in the Fourier Domain example
This example shows the potential of using graphical user interfaces, for a very
simple application. With this program we can:
* Open any image,
* See the image, and the magnitude of its Fourier transform,
* Resize the image,
* Apply Gaussian low pass / high pass filters of different radious.

The half-tone image provided is the one used to test the algorithm. On it,
several spots of sine waves have been placed, producing a dotted image.
As a result, the driver face and its plate are not visible.

By putting adequate filters at each spot, and by applying a large low pass filter
around the center, the image quality can be considerably improved.

# Application screenshot
![app screenshot](/FourierFilteringProject/images/FourierImage.png)
