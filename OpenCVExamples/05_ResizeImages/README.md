# Load and resize images example
In this case, we take a color image, and we resize it. We provide two examples,
one to reduce the image size, and another one to increase it. In both examples,
the function used is the same. The only difference is the final dimension argument.

Then, as in the other examples, we show the original image, and the resized images,
in order to compare them.

It is worth to mention that, depending on our requirements, we need to choose
the correct interpolation algorithm. This is particularly important when we
increase an image size. In that case, when we expand an image, we have the original
pixels that will we placed far away one each other, with regard the original image.
So, there will be pixels in the middle that we have to fill with something.
An interpolation algorithm is the one that decides how to compute those missing
pixels. OpenCV offers several of those algorithms for resizing images, and they
provide different properties of the output image. In order to decide which one
we pick, we have to read about them, and take the one that better fits to our needs.

In this example, we choose the Linear interpolation. We propose the reader
to pick an small image (100x100 or even 50x50 pixels) and resize it to have a big size.
Then choose different interpolations algorithms and see how the output looks like.

# Application screenshot
![app screenshot](/OpenCVExamples/05_ResizeImages/images/ResizedImages.png)