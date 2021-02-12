import cv2
import os

import numpy as np
import matplotlib.pyplot as plt

root_dir = os.path.dirname(os.path.realpath(__file__))

def increase_brightness_lut():
    '''
    We create a LUT that increases the brightness.

    Returns:
        LUT with 256 entries, from 0 until 255.
    '''
    # We create a line at 45 degrees: starting from zero, we create an array
    # with 256 entries, where the increase between two consecutive elements is 1.
    lut = np.arange(0, 256, 1)
    # We slide the LUT by 40 in the upwards direction
    lut = lut + 40.0
    # We truncate the elements higher than 255 to be 255 (saturation area)
    lut[lut > 255] = 255
    # We reconvert the LUT to be 8-bits coded.
    return np.array(lut, dtype=np.uint8)

def increase_contrast_lut():
    '''
    We create a LUT that increases the contrast.

    Returns:
        LUT with 256 entries, from 0 until 255.
    '''
    # we start all the LUT as zeros
    lut = np.zeros(256)
    # We set all the elements between 50 and 200 to be a line with slope 255 / (200 - 50)
    lut[50:200] = np.arange(0, 255, 1.7) + 0.5
    # We set all the elements starting from index 200 to be 255 (saturation area)
    lut[200:] = 255
    # We reconvert the LUT to be 8-bits coded.
    return np.array(lut, dtype=np.uint8)

def gamma_correction_lut(gamma_value):
    '''
    We create a LUT that follows the gamma function.

    Args:
        gamma_value: Exponent used for the gamma function

    Returns:
        LUT with 256 entries, from 0 until 255.
    '''
    # We create a line at 45 degrees: starting from zero, we create an array
    # with 256 entries, where the increase between two consecutive elements is 1.
    input_array = np.arange(0, 256, 1)
    # We return an array of values from 0 until 255, with the values of the gamma function:
    #                       Io = 255 * (I / 255)^gamma
    # where I is the input intensity value and I0 is the output intensity value.
    # We return an array coded in 8 bits
    return np.array(255 * np.power((input_array / 255.0), gamma_value), dtype=np.uint8)

def plot_lut(lut, title):
    '''
    Function to plot a given LUT.

    Args:
        lut: LUT to be plot
        title: Title to add to the plot
    '''
    # We start a figure to plot
    plt.figure()
    # We plot the LUT as a curve
    plt.plot(lut)
    # We limit the X axis to be between 0 and 255.
    plt.xlim(0, 255)
    # We add the given title to the plot
    plt.title(title)
    # We show the plot's grid
    plt.grid()
    # We add labels to the X and Y axis
    plt.xlabel("Input level")
    plt.ylabel("Output level")
    # We show the graph in non-blocking mode.
    plt.show(block=False)

def apply_lut(img, lut):
    '''
    Function to apply a given LUT. This function works for gray-level images.

    Args:
        img: Input image to which we will apply the transformation
        lut: LUT to be applied

    Returns:
        Matrix coded in 8-bits that is the result of applyting the given LUT
        to the input image.
    '''
    # We convert the input lut to be a numpy array, in order to profit the indexing
    # property of the NumPy arrays.
    int_lut = np.array(lut, dtype=np.uint8)
    return int_lut[img]

def main():
    '''
    Main function of the Python script.
    It will open an image, and it will apply a series of LUT to see their effect
    on it.
    '''
    # We define the image filepath we want to load
    color_image_filepath = os.path.join(root_dir, 'images', 'Lenna.png')
    # We load the image, and we pass the flag to load it as in gray-level mode.
    gray_img = cv2.imread(color_image_filepath, cv2.IMREAD_GRAYSCALE | cv2.IMREAD_ANYDEPTH)
    # We check if imread was able to find and open the image.
    if gray_img is None:
        print("We couldn't load the image located at {}".format(color_image_filepath))
        return

    # We plot the LUT that increases the brightness
    plot_lut(increase_brightness_lut(), "Increase brightness LUT")
    # We plot the LUT that increases the contrast
    plot_lut(increase_contrast_lut(), "Increase contrast LUT")

    # We plot the LUT that corresponds to the gamma correction
    gamma = 2.1
    plot_lut(gamma_correction_lut(gamma), "Gamma correction LUT for gamma = {}".format(gamma))

    # We plot the images
    # Original image
    gl_window_name = 'Gray-level image'
    cv2.namedWindow(gl_window_name, cv2.WINDOW_NORMAL)
    cv2.imshow(gl_window_name, gray_img)

    # Original image after applying the increasing brightness LUT
    gl_window_name = 'Increase brightness'
    cv2.namedWindow(gl_window_name, cv2.WINDOW_NORMAL)
    cv2.imshow(gl_window_name, apply_lut(gray_img, increase_brightness_lut()))

    # Original image after applying the increasing contrast LUT
    gl_window_name = 'Increase contrast'
    cv2.namedWindow(gl_window_name, cv2.WINDOW_NORMAL)
    cv2.imshow(gl_window_name, apply_lut(gray_img, increase_contrast_lut()))

    # Original image after applying the gamma LUT
    gl_window_name = 'Gamma correction'
    cv2.namedWindow(gl_window_name, cv2.WINDOW_NORMAL)
    cv2.imshow(gl_window_name, apply_lut(gray_img, gamma_correction_lut(gamma)))

    # We always need these lines
    key = cv2.waitKey()
    while chr(key) != 'q' and chr(key) != 'Q':
        key = cv2.waitKey()

    # we close all the opened OpenCV windows before exiting.
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()