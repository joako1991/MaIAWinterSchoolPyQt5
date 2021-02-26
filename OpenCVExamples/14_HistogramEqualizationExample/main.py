import cv2
import os
import numpy as np

root_dir = os.path.dirname(os.path.realpath(__file__))

def get_histo(img):
    '''
    Compute the histogram of an image. This function considers the image has
    a single channel.

    Args:
        img: Input image from which we want to compute the histogram

    Returns:
        Vector of N entries, where N is the amount of possible levels in the image.
        This value depends on the data type used to represent the image.
        If the image is coded in 8 bits, N = 256. If it is coded in 16 bits,
        N = 65536. In this vecor, each position represents a gray-level
        value, and the content of each position is the amount of pixels that
        have that value.
    '''
    np_img = np.array(img)
    amount_bits = int(8.0 * np_img.nbytes / np_img.size)
    hist = np.zeros(np.power(2, amount_bits))
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            hist[img[i,j]] += 1
    return hist

def compute_acumm_prob_func(hist, rows, cols):
    '''
    Compute the accumulative probability function of a given histogram.

    Args:
        hist: Histogram of a certain image.
        rows: Amount of rows of the image from which the histogram belongs to.
        cols: Amount of columns of the image from which the histogram belongs to.

    Returns:
        Vector of as meny entries as in the histogram, in which each position
        represents a gray-level value, and the content of each position is the
        probability that a pixel have a value less or equal to this position.
    '''
    apf = np.zeros(len(hist), dtype=np.float32)
    norm_hist = np.array(hist, dtype=np.float32) / (rows * cols)
    apf[0] = norm_hist[0]
    for i in range(1, len(norm_hist)):
        apf[i] = apf[i-1] + norm_hist[i]
    return apf

def equalize_img_hist(img):
    '''
    Apply the histogram equalization algorithm. This function does not depends
    if the image is color or gray-level. If it is gray-level, it will apply the
    algorithm once. If the image is color, it will apply the algorithm three times,
    once per channel.

    Args:
        img: Input image that we want to equalize

    Returns:
        Image, with the same shape as the input image. This output image has
        its histogram equalized (or the three channels equalized seperately,
        if it is color).
    '''
    cloned_img = np.array(img)
    channels = 3
    if len(cloned_img.shape) == 2:
        cloned_img = np.reshape(img, (img.shape[0], img.shape[1], 1))
        channels = 1
    elif len(cloned_img.shape) != 3:
        assert(0)

    for i in range(channels):
        channel_hist = get_histo(cloned_img[:,:,i])

        apf = np.array(255.0 * compute_acumm_prob_func(channel_hist, cloned_img.shape[0], cloned_img.shape[1]), dtype=np.uint8)
        cloned_img[:,:,i] = apf[cloned_img[:,:,i]]

    return np.reshape(cloned_img, img.shape)

def example_histogram_equalization_rgb(img_filepath):
    '''
    This example shows how to apply the histogram equalization operation, and its result,
    to an RGB image. The histogram equalization in this case is done in the
    RGB space, so each channel is equalized separately. As a result, we have
    the problem of fake colors in the image.

    Args:
        img_filepath: Filepath of the image we want to apply the histogram
        equalization algorithm
    '''
    # We load the image, and we pass the flag to load it as in gray-level mode.
    img = cv2.imread(img_filepath, cv2.IMREAD_ANYCOLOR | cv2.IMREAD_ANYDEPTH)
    # We check if imread was able to find and open the image.
    if img is None:
        print("We couldn't load the image located at {}".format(img_filepath))
        return

    # We apply the RGB histogram equalization algorithm
    output_img = equalize_img_hist(img)

    # We show the original image and the equalized image
    win_name = 'Original image'
    cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)
    cv2.imshow(win_name, img)

    win_name = 'Equalized histogram image in RGB'
    cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)
    cv2.imshow(win_name, output_img)

    # We always need these lines
    key = cv2.waitKey()
    while chr(key) != 'q' and chr(key) != 'Q':
        key = cv2.waitKey()

    # we close all the opened OpenCV windows before exiting.
    cv2.destroyAllWindows()


def example_histogram_equalization_hsv(img_filepath):
    '''
    This example shows how to apply the histogram equalization operation, and its result,
    to an RGB image. The histogram equalization in this case is done in the
    HSV space, we equalize only the value channel, leaving the hue and saturation
    channels untouched.

    Args:
        img_filepath: Filepath of the image we want to apply the histogram
        equalization algorithm
    '''
    # We load the image, and we pass the flag to load it as in gray-level mode.
    img = cv2.imread(img_filepath, cv2.IMREAD_ANYCOLOR | cv2.IMREAD_ANYDEPTH)
    # We check if imread was able to find and open the image.
    if img is None:
        print("We couldn't load the image located at {}".format(img_filepath))
        return

    # We convert the image into the HSV space
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # We apply the histogram equalization algorithm. In this case, only the value
    # channel is used, which can be accessed by doing hsv_img[:,:,2],
    # since hsv_img[:,:,0] is the hue, and hsv_img[:,:,1] is the saturation
    hsv_img[:,:,2] = equalize_img_hist(hsv_img[:,:,2])
    # We reconvert the image into the BGR space in order to show it.
    output_img = cv2.cvtColor(hsv_img, cv2.COLOR_HSV2BGR)

    # We show the original image and the equalized image
    win_name = 'Original image'
    cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)
    cv2.imshow(win_name, img)

    win_name = 'Equalized histogram image in HSV'
    cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)
    cv2.imshow(win_name, output_img)

    # We always need these lines
    key = cv2.waitKey()
    while chr(key) != 'q' and chr(key) != 'Q':
        key = cv2.waitKey()

    # we close all the opened OpenCV windows before exiting.
    cv2.destroyAllWindows()

def main():
    # We define the image filepath we want to load
    img_filepath = os.path.join(root_dir, 'images', 'Lenna.png')

    example_histogram_equalization_rgb(img_filepath)
    example_histogram_equalization_hsv(img_filepath)

if __name__ == '__main__':
    main()