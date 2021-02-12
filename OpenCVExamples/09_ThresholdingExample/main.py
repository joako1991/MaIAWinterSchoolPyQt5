import cv2
import os

import numpy as np

root_dir = os.path.dirname(os.path.realpath(__file__))

def threshold_image(img, threshold):
    '''
    This function creates a binary image based on the gray-level image.
    If the pixel intensity is higher than the threshold, the image value
    is set to 255. If not, it is set to 0.

    Args:
        img: Input image to be binarized
        threshold: Integer value, between 0 and 255, that defines the threshold value

    Returns:
        Binary image
    '''
    # We convert the image into a numpy array, to ensure we can use the indexing property of
    # NumPy arrays
    np_img = np.array(img)
    # In all the places where the image value is higher than the threshold, we set it to 255
    np_img[np_img > threshold] = 255
    # In all the places where the image value is lower or equal than the threshold, we set it to 0
    np_img[np_img <= threshold] = 0
    # We return the binarized image
    return np_img

def main():
    # We define the image filepath we want to load
    color_image_filepath = os.path.join(root_dir, 'images', 'Lenna.png')
    # We load the image, and we pass the flag to load it as in gray-level mode.
    gray_img = cv2.imread(color_image_filepath, cv2.IMREAD_GRAYSCALE | cv2.IMREAD_ANYDEPTH)
    # We check if imread was able to find and open the image.
    if gray_img is None:
        print("We couldn't load the image located at {}".format(color_image_filepath))
        return

    # We threshold the image
    binary = threshold_image(gray_img, 100)

    # We show the loaded gray-level image
    gl_window_name = 'Gray-level image'
    # We create a namedWindow, with the flag cv2.WINDOW_NORMAL in order to be able
    # to resize the image as we want, with the mouse
    cv2.namedWindow(gl_window_name, cv2.WINDOW_NORMAL)
    # We show the image.
    cv2.imshow(gl_window_name, gray_img)

    # We show the binarized image
    gl_window_name = 'Binary image'
    # We create a namedWindow, with the flag cv2.WINDOW_NORMAL in order to be able
    # to resize the image as we want, with the mouse
    cv2.namedWindow(gl_window_name, cv2.WINDOW_NORMAL)
    # We show the image.
    cv2.imshow(gl_window_name, binary)

    # We always need these lines
    key = cv2.waitKey()
    while chr(key) != 'q' and chr(key) != 'Q':
        key = cv2.waitKey()

    # we close all the opened OpenCV windows before exiting.
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()