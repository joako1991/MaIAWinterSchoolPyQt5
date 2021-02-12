# Convolution example
This example implements two ways to solve the convolution operation. One is the
way by definition, in which we follow the algorithm shown in the theory.
In the other case, we implement the shift-multiply algorithm, that reduces the
execution time considerable, since we profit of the indexing handling of numpy
arrays, and instead of iterating over all the image, we only iterate over the
kernel. It can be shown that both results are correct with the convolution
definition.

The convolution by definition takes 1.79 seconds, and the shift-multiply
takes 0.17 seconds, for the same kernel and the same image. This means that
the shift-multiply operation is 950% times faster.

Then, we added some kernels and we apply them to the same image to see their effect.
We included a smoothing kernel, a laplacian kernel, and a gaussian kernel. We
also show the results. The gaussian and laplacian filters are 3x3, and the smoothing
filter is 21x21. Can you see a difference in shape between the smoothed image
(using the definition convolution and the Gaussian filtered image?)

In this implementation, take special care to the the data-types each moment:
There are several moments in which the images are converted into float
values to avoid the overflow, and then they are reconverted into 8 bits
images (why in each case we have to do that?).

# Application screenshot
![app screenshot](/OpenCVExamples/07_Convolution/images/ConvolutionExample.png)