import cv2
import os
import sys
import numpy as np
import time

import matplotlib.pyplot as plt

root_dir = os.path.dirname(os.path.realpath(__file__))

def alternative_histogram_computation(img):
    '''
    Compute the image provided. In order to have an histogram, the image must
    not be empty, and it must be a gray-level image.

    Args:
        img: Input gray-level image from which we want to compute the histogram

    Returns:
        None if the image is not gray-level, or if it is empty. It returns
        an array with as many elements as possible gray-levels can be in the image
        (it depends on the data type of the input image). Each element i
        of this array represents how many pixels in the image have the level
        i.
    '''
    # We convert the image into a numpy array to be sure it is an array and not
    # a list. This give us several functions that are not availables for normal lists.
    img = np.array(img)
    # We check the image is not empty
    if img.size:
        # We check if the image is gray-level (if it would be color, the shape property
        # will have 3 elements instead of 2: (rows, columns, channels))
        if len(img.shape) == 2:
            # We check the amount of bits are used to represent the data (8 * amuont of bytes)
            amount_bits = img[0,0].nbytes * 8
            # We check how many levels (or bins) are possible with this amount of bits
            amount_bins = np.power(2, amount_bits)
            # We compute the histogram using the NumPy function. bins is the
            # range, or list of values that corresponds to the possible gray-levels
            # in the image.
            myHist = np.histogram(img, bins=range(amount_bins))
            # We return the first element, which corresponds to the histogram.
            # The second element of this list is the array with the bins of the
            # histogram
            return myHist[0]

        else:
            print("ERROR: The provided image is not gray-level!!!. Its shape is {}".format(img.shape))
            return None
    else:
        print("ERROR: The image is empty!!!")
        return None

def compute_histogram(img):
    '''
    Compute the image provided. In order to have an histogram, the image must
    not be empty, and it must be a gray-level image.

    Args:
        img: Input gray-level image from which we want to compute the histogram

    Returns:
        None if the image is not gray-level, or if it is empty. It returns
        an array with as many elements as possible gray-levels can be in the image
        (it depends on the data type of the input image). Each element i
        of this array represents how many pixels in the image have the level
        i.
    '''
    # We convert the image into a numpy array to be sure it is an array and not
    # a list. This give us several functions that are not availables for normal lists.
    img = np.array(img)
    # We check the image is not empty
    if img.size:
        # We check if the image is gray-level (if it would be color, the shape property
        # will have 3 elements instead of 2: (rows, columns, channels))
        if len(img.shape) == 2:
            # We check the amount of bits are used to represent the data (8 * amuont of bytes)
            amount_bits = img[0,0].nbytes * 8
            # We check how many levels (or bins) are possible with this amount of bits
            amount_bins = np.power(2, amount_bits)
            print("The image has {} bins".format(amount_bins))

            # We create a linear array, with the amount of possible levels, and we
            # put zeros on each position.
            histogram = np.zeros(amount_bins)

            for i in range(img.shape[0]):
                for j in range(img.shape[1]):
                    # We check each pixel in the image. The intensity value at the
                    # position (i,j) is given by img[i,j]. If we code the image
                    # in 8 bits, img[i,j] is a value between 0 and 255. Its
                    # value is used to access to the array position of the histogram.
                    # So, to take into account this pixel value, we increase by one
                    # the content of the histogram at the position corresponding to
                    # that pixel value.
                    pixel_value = img[i,j]
                    histogram[pixel_value] += 1

            # We return the computed histogram
            return histogram
        else:
            print("ERROR: The provided image is not gray-level!!!. Its shape is {}".format(img.shape))
            return None
    else:
        print("ERROR: The image is empty!!!")
        return None

def show_histogram(hist, title):
    '''
    Show the provided histogram as a bar plot.
    NOTE: The plot has been configured to not block. That means you have to avoid
    the script to exit automatically after this call (either by using cv2.waitKey
    or use input('MY_MSG') to wait for the user to press a key). If you do not
    block the code from exiting, the plot will open and close quickly, and you
    won't see anything.

    To create the plot, we use the library matplotlib, since in a few lines
    we can have the plot we want.

    Args:
        title: String with the plot title we want to put on top of the plot.
    '''
    # We create a figure to show our plot
    plt.figure()
    # We create a range of values, i.e., a lines of values from 0 until the specified
    # value, separated one unit one each other. The prototype of range is:
    # range(start, stop), and that will create a line of values in the interval
    # [start, stop]. Both, start and stop must be integers values. If you want to
    # create a line of float values, separated by a given step, check the function
    # numpy.arange(start, stop, step)
    x = range(len(hist))
    # We add to our figure the bar plot. The first argument corresponds to the
    # X axis values, the second one corresponds to the Y values, and width is
    # the width of the bars
    plt.bar(x, hist, width=0.8)
    # We add a grid in the graph
    plt.grid()
    # We add the specified title
    plt.title(title)
    # We add labels to the X and Y axis, to identify which variables each axis represents
    plt.xlabel("Gray-level value")
    plt.ylabel("# pixels")
    # We limit the X axis to be between 0 and the maximum gray-level value
    plt.xlim(0, len(hist) - 1)
    # We show the created plot. block=False means that this function will show
    # and return. If we want to stop the execution here, we have to put
    # block=True
    plt.show(block=False)

def main():
    '''
    Main function. We load an image as a gray-level image, and we compute and show
    its histogram.
    '''
    # We define the image filepath we want to load
    color_image_filepath = os.path.join(root_dir, 'images', 'Lenna.png')
    # We load the image, and we pass the flag to load it as in gray-level mode.
    gray_img = cv2.imread(color_image_filepath, cv2.IMREAD_GRAYSCALE | cv2.IMREAD_ANYDEPTH)
    # We check if imread was able to find and open the image.
    if gray_img is None:
        print("We couldn't load the image located at {}".format(color_image_filepath))
        return

    print("Gray-level image shape: {}".format(gray_img.shape))

    begin = time.time()
    # We compute the histogram using the function define above.
    hist = compute_histogram(gray_img)
    print("Defintion implementation: {}".format(time.time() - begin))

    begin = time.time()
    # We compute the histogram using this alternative implementation, which makes
    # use of a numpy function
    hist2 = alternative_histogram_computation(gray_img)
    print("Alternative implementation: {}".format(time.time() - begin))

    # We check if the histogram was computed correctly or not.
    if not hist is None:
        # If the histogram has been computed correctly, we show it.
        show_histogram(hist, 'Gray-level image histogram')

    # We check if the alternative histogram was computed correctly or not.
    if not hist is None:
        # If the histogram has been computed correctly, we show it.
        show_histogram(hist2, 'Alternative Gray-level image histogram')

    # We show the loaded gray-level image
    gl_window_name = 'Gray-level image'
    # We create a namedWindow, with the flag cv2.WINDOW_NORMAL in order to be able
    # to resize the image as we want, with the mouse
    cv2.namedWindow(gl_window_name, cv2.WINDOW_NORMAL)
    # We show the image.
    cv2.imshow(gl_window_name, gray_img)

    # We always need these lines
    key = cv2.waitKey()
    while chr(key) != 'q' and chr(key) != 'Q':
        key = cv2.waitKey()

    # we close all the opened OpenCV windows before exiting.
    cv2.destroyAllWindows()
    return

if __name__ == '__main__':
    main()