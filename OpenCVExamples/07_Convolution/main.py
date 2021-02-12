import cv2
import os
import numpy as np

import time

root_dir = os.path.dirname(os.path.realpath(__file__))

def apply_convolution_shift_multiply(image, kernel):
    '''
    Make the convolution of the image with the given kernel. This function
    is made for 2D signals, not for 1D signals.

    The algorithm implemented is called Add-shift-multiply. It does not reduce
    the image size once applied.

    This function works for both, gray-level and color images, and it does not
    require to flip the kernel.

    Args:
        image: Input image
        kernel: Input kernel (filter)

    Returns:
        Result of doing the convolution of image and the given kernel
    '''
    # We convert the input image as an image of floats, to avoid overflow of the
    # numbers.
    np_img = np.array(image, dtype=np.float)
    # If the image is gray-level, we add an indexation level, so the image
    # instead of having a shape (rows, columns) will be (rows, columns, 1)
    if len(np_img.shape) == 2:
        np_img = np_img.reshape(np_img.shape + (1,))
    # We ensure the kernel is a numpy array
    np_h = np.array(kernel)

    # We extract the image shape components, to reduce the amount of letters per instruction
    img_rows = np_img.shape[0]
    img_cols = np_img.shape[1]
    bands = np_img.shape[2]

    # We extract the kernel shape components, to reduce the amount of letters per instruction
    h_rows = np_h.shape[0]
    h_cols = np_h.shape[1]
    # Initialize the output image, to be bigger than the original image.
    # If the input image have a size RxC and the kernel, MxN, the output image
    # size will be:
    #           R' x C' = (R + M - 1, C + N - 1 )
    A = np.zeros([img_rows + h_rows - 1, img_cols + h_cols - 1, bands])

    # Instead of shifting the image, we make use of the indexing system of NumPy
    # arrays, and we only move over the kernel size, which is generally smaller
    # than the image.
    for m in range(h_rows):
        for n in range(h_cols):
            # We take a sub-image from A, and we add to it the entire original image
            # multiplied with one of the weights of the kernel.
            A[m:m+img_rows,n:n+img_cols,:] += (np_img * np_h[m,n])

    # We compute the coordinates of the starting point of the valid image.
    center_x = int(h_rows / 2.0)
    center_y = int(h_cols / 2.0)

    # From the output image created, we extract the center image.
    return np.array(A[center_x:center_x + img_rows, center_y:center_y + img_cols, :], dtype=np.int)

def apply_convolution(img, kernel):
    '''
    Make the convolution of the image with the given kernel. This function
    is made for 2D signals, not for 1D signals.

    The algorithm implemented executes the convolution by definition, and its
    does not do zero padding, which means the output size will be reduce.

    Args:
        image: Input image
        kernel: Input kernel (filter)

    Returns:
        Result of doing the convolution of image and the given kernel
    '''
    # We flip the kernel in all the axis (horizontally and vertically)
    kernel = np.flip(kernel)
    print("Kernel size: {}".format(kernel.shape))
    # We create an array with the output image size:
    # if the input is RxC and the kernel is MxN, the output image will have a size
    #                   R'x C' = (R - M + 1, C - N + 1)
    output_size = [img.shape[0] - kernel.shape[0] + 1, img.shape[1] - kernel.shape[1] + 1]
    # We create an empty output image, filled with zeros
    output = np.zeros(output_size)

    # We travel over all the output image (pixel by pixel).
    for i in range(output_size[0]):
        for j in range(output_size[1]):
            # For each pixel in the output image, we compute which are the pixels
            # involved at each convolution step
            # We compute the range of rows
            start_row = i
            end_row = i + kernel.shape[0]
            # We compute the range of columns
            start_col = j
            end_col = j + kernel.shape[1]
            # We compute the linear combination between the kernel
            # and the corresponding piece of image. For it, we multiply pixel-wise
            # the pixels involved and the kernel. That will give us another kernel.
            # Then we sum all the values in that new kernel. The result is placed in
            # the position i,j of the output image.
            output[i,j] = int(np.sum(np.multiply(kernel, img[start_row:end_row, start_col:end_col])))
    return output

def get_gaussian_kernel():
    '''
    Get a 3x3 Gaussian filter to the image.

    Returns:
        Kernel to apply gaussian filtering
    '''
    return np.array([[1.0,2.0,1.0],[2.0,4.0,2.0],[1.0,2.0,1.0]]) / 16.0

def get_smoothing_filter(kernel_size):
    '''
    Get a square low-pass filter of the specified size.

    Args:
        kernel_size: Integer that represents the amount of columns
            and rows that the kernel will have

    Returns:
        Requested smoothing kernel
    '''
    if kernel_size % 2 == 0:
        raise ValueError("The kernel size must be an odd number. Provided: {n}".format(n=kernel_size))
    factor = 1.0 / (kernel_size * kernel_size)
    kernel_shape = np.array((kernel_size, kernel_size))
    return np.ones(kernel_shape) * factor

def get_laplace_kernel():
    '''
    Get a laplacian edge-detector kernel

    Returns:
        Requested kernel
    '''
    return np.array([[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]], dtype=np.float)

def normalize_img(img, new_min_val, new_max_val):
    '''
    Normalize the image to be in the desired range of values.

    Args:
        img: Input image to be normalized
        new_min_val: Minimum value we want the new image to have
        new_max_val: Maximum value we want the new image to have

    Returns:
        Normalized image
    '''
    # We extract the maximum and minimum values in the input image
    imgMin = np.min(img)
    imgMax = np.max(img)

    print("Image max val: {}".format(imgMax))
    print("Image min val: {}".format(imgMin))

    # We convert the input image into a NumPy array to profit of the matrix by
    # constant multiplication, and sum, and we convert it into float to avoid
    # overflow problems
    img = np.array(img, dtype=np.float32)
    # We compute the histogram normalization as:
    #               Output = [ (input - img_min_val) * (new_max_val - new_min_val) / (img_max_val - img_min_val) ] + new_min_val
    output = np.array(((img - imgMin) * ((new_max_val - new_min_val) / (imgMax - imgMin))) + new_min_val, dtype=np.uint8)

    return output

def main():
    '''
    Main function. We load an image as a gray-level image, and we apply
    a kernel to it.
    '''
    # We define the image filepath we want to load
    color_image_filepath = os.path.join(root_dir, 'images', 'Lenna.png')
    # We load the image, and we pass the flag to load it as in gray-level mode.
    gray_img = cv2.imread(color_image_filepath, cv2.IMREAD_GRAYSCALE | cv2.IMREAD_ANYDEPTH)
    # We check if imread was able to find and open the image.
    if gray_img is None:
        print("We couldn't load the image located at {}".format(color_image_filepath))
        return

    # We test both algorithms, shift-multiply and definition algorithm with
    # a kernel of 21x21
    begin = time.time()
    smoothed_img = apply_convolution_shift_multiply(gray_img, get_smoothing_filter(21))
    print("The Shift-multiply algorithm takes {} seconds".format(time.time() - begin))
    begin = time.time()
    smoothed_img = apply_convolution(gray_img, get_smoothing_filter(21))
    print("The definition algorithm takes {} seconds".format(time.time() - begin))

    # We test the shift-multiply algorithm with a gaussian filter 3x3
    gaussian_filtered_img = apply_convolution_shift_multiply(gray_img, get_gaussian_kernel())
    # We test the shift-multiply algorithm with a laplacian filter 3x3
    laplacian_filtered_img = apply_convolution_shift_multiply(gray_img, get_laplace_kernel())
    # Since the laplacian involves negative and positive values, in order to show
    # the output image, we make the absolute value of this image, and we normalize
    # it to be in the range 0 to 255. This way, the zero will stay being zero.
    # If we normalize the original output, the zero will be in the middle of
    # the image, giving the background a gray aspect that is not desired.
    absolute_lapacian = np.absolute(laplacian_filtered_img)
    absolute_lapacian = normalize_img(absolute_lapacian, 0, 255)

    ################ We show all the results ################
    # We show the loaded gray-level image
    gl_window_name = 'Gray-level image'
    # We create a namedWindow, with the flag cv2.WINDOW_NORMAL in order to be able
    # to resize the image as we want, with the mouse
    cv2.namedWindow(gl_window_name, cv2.WINDOW_NORMAL)
    # We show the image.
    cv2.imshow(gl_window_name, gray_img)

    # We show the smoothed image
    gl_window_name = 'Smoothed image'
    # We create a namedWindow, with the flag cv2.WINDOW_NORMAL in order to be able
    # to resize the image as we want, with the mouse
    cv2.namedWindow(gl_window_name, cv2.WINDOW_NORMAL)
    # We show the image.
    cv2.imshow(gl_window_name, np.array(smoothed_img, dtype=np.uint8))

    # We show the gaussian filtered image
    gl_window_name = 'Gaussian filtered image'
    # We create a namedWindow, with the flag cv2.WINDOW_NORMAL in order to be able
    # to resize the image as we want, with the mouse
    cv2.namedWindow(gl_window_name, cv2.WINDOW_NORMAL)
    # We show the image.
    cv2.imshow(gl_window_name, np.array(gaussian_filtered_img, dtype=np.uint8))

    # We show the Laplacian filtered image
    gl_window_name = 'Laplacian filtered image'
    # We create a namedWindow, with the flag cv2.WINDOW_NORMAL in order to be able
    # to resize the image as we want, with the mouse
    cv2.namedWindow(gl_window_name, cv2.WINDOW_NORMAL)
    # We show the image.
    cv2.imshow(gl_window_name, np.array(absolute_lapacian, dtype=np.uint8))

    # We always need these lines
    key = cv2.waitKey()
    while chr(key) != 'q' and chr(key) != 'Q':
        key = cv2.waitKey()

    # we close all the opened OpenCV windows before exiting.
    cv2.destroyAllWindows()
    return

if __name__ == '__main__':
    main()