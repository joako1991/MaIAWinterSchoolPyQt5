import cv2
import os

import numpy as np
# This module only contains one variable with a bunch of colors in the HSV space
from colors import hsv_label_colors

root_dir = os.path.dirname(os.path.realpath(__file__))

def threshold_image(img, threshold):
    '''
    This function thresholds a gray-scale image. At each pixel, if its value
    is higher than the threshold, that pixel becomes one, if not, it becomes zero.

    Args:
        img: Input gray-scale image to be thresholded.
        threshold: Integer value, that defines the threshold.

    Returns:
        Binary image, result of thresholding the input with the given threshold.
    '''
    # We create an empty binary image with zeros only
    binary = np.zeros(img.shape)
    # We place ones only in the pixels where the original image values are
    # higher than the threshold
    binary[img > threshold] = 1
    return np.array(binary, dtype=np.uint8)

def get_connected_labeled_image(img, conn):
    '''
    We label an image in different elements, using the connected-components
    algorithm from OpenCV.

    This function allows to choose the 4- or 8-connected components patternt.

    Args:
        img: Binary image to be labeled (only zeros and 1s are allowed)
        conn: Connected components pattern (integer value, only 4 or 8 are valid options)

    Returns:
        Image where each pixel is labeled with an integer value (0 for the background,
        1,2,3,4,etc for the different objects).
    '''
    # We check if the image is binary filled only with 0s and 1s
    assert(np.max(img) == 1 and np.min(img) == 0)
    # We check that the input connected pattern is 4 or 8
    assert(conn == 4 or conn == 8)
    # We apply the OpenCV connected components algorithm. The output of this algorithm
    # is a tuple: The first element is the amount of labels found, and the second
    # element is the labeled image.
    labeled = cv2.connectedComponents(img, connectivity=conn)

    print("The image has been labeled with {p}-connected pattern. {l} labels has been found".format(p=conn, l=labeled[0]))
    # We return all the labeled image only
    return labeled[1]

def create_color_image_from_labeled(labeled_img):
    '''
    We convert a labeled image (image obtained after applying the ConnectedComponents
    algorithm) into a colored image.

    Args:
        labeled_img: Image where each pixel contains a number that identifies certain
        class. All the pixels that belongs to the same class (i.e., have the same
        value) will be painted with the same color.

    Returns:
        RGB image where all the pixels that belong to the same class are painted
        with the same color.
    '''
    # We create a color image: It will have the same size as the input image, but
    # it will contain 3 channels
    output = np.zeros(labeled_img.shape + (3,), dtype=np.uint8)
    # We determine the amount of labels in the image. We add one since the for loop
    # does not consider the last element
    amount_labels = np.max(labeled_img) + 1

    # We determine how many colors we imported from the module colors.py
    amount_colors = len(hsv_label_colors)
    print("There are {} labels".format(amount_labels))

    # We label all the pixels. For all the labels, we assign the same colors to
    # the pixels that have the same label.
    for i in range(1, amount_labels):
        # We determine the color to use. If we have more labels than colors,
        # we restart the counter, i.e., different classes will have the same
        # color, but since they will be far away one each other, it will be
        # easy to identify them
        idx = i % amount_colors
        output[labeled_img == i] = hsv_label_colors[idx]

    # Since the assigned colors are in HSV space, we convert them into BGR
    # system to show the image in OpenCV
    return cv2.cvtColor(output, cv2.COLOR_HSV2BGR)

def get_image_example():
    '''
    Get the image shown in the example used in the theory file.
    '''
    img = np.array([[0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 0],
                    [1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1],
                    [1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0]], dtype=np.uint8)
    return img

def main():
    '''
    Main function of the Python script.

    It will load a gray-level image, it will binarize it, and label it using
    the connected-components algorithm. Then it shows the images created during this
    process.
    '''
    color_image_filepath = os.path.join(root_dir, 'images', 'metal.png')
    gray_img = cv2.imread(color_image_filepath, cv2.IMREAD_GRAYSCALE | cv2.IMREAD_ANYDEPTH)
    # We check if imread was able to find and open the image.
    if gray_img is None:
        print("We couldn't load the image located at {}".format(color_image_filepath))
        return

    binary = threshold_image(gray_img, 120)

    gl_window_name = 'Gray-level image'
    cv2.namedWindow(gl_window_name, cv2.WINDOW_NORMAL)
    cv2.imshow(gl_window_name, gray_img)

    # NOTE: If you want to run the example of the theory, uncomment the line below.
    # binary = get_image_example()

    labeled_image = get_connected_labeled_image(binary, 4)
    colored_image = create_color_image_from_labeled(labeled_image)

    gl_window_name = 'Binary images'
    cv2.namedWindow(gl_window_name, cv2.WINDOW_NORMAL)
    cv2.imshow(gl_window_name, 255 * binary)

    gl_window_name = 'Labeled image'
    cv2.namedWindow(gl_window_name, cv2.WINDOW_NORMAL)
    cv2.imshow(gl_window_name, colored_image)

    # These lines we need them always
    key = cv2.waitKey()
    while chr(key) != 'q' and chr(key) != 'Q':
        key = cv2.waitKey()

    cv2.destroyAllWindows()
    return

if __name__ == '__main__':
    main()