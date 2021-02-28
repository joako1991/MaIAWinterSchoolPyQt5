import cv2
import os
import numpy as np
from bar_code import BarCode
import copy

root_dir = os.path.dirname(os.path.realpath(__file__))

def main():
    '''
    Main function of the Python Script. This function will open a code bar
    image, in UPC-A format, and it will decode it. The result will be printed
    into the terminal.
    '''
    # We define our image filepath
    img_filepath = os.path.join(root_dir, 'images', 'barcode.png')
    # img_filepath = os.path.join(root_dir, 'images', 'turned_barcode.png')
    # img_filepath = os.path.join(root_dir, 'images', 'vertical_code.png')

    # We load our image as a grayscale image
    img = cv2.imread(img_filepath, cv2.IMREAD_GRAYSCALE | cv2.IMREAD_ANYDEPTH)
    # We check if imread was able to find and open the image.
    if img is None:
        print("We couldn't load the image located at {}".format(img_filepath))
        return
    print("Image shape: {}".format(img.shape))

    bar_code_detector = BarCode()

    # For the horizontal bars
    bars_code_pixels = copy.deepcopy(img[35,:])

    # For the vertical bars
    # bars_code_pixels = copy.deepcopy(img[:,35])

    # We convert the image into binary, with two values, 0 or 1.
    bars_code_pixels[bars_code_pixels > 0] = 1
    bars_code_pixels = 1 - bars_code_pixels
    bar_code_detector.decode(bars_code_pixels)

    # We show the bars code.
    win_name = 'Bars code'
    cv2.namedWindow(win_name, cv2.WINDOW_NORMAL);
    cv2.imshow(win_name, img);

    # We always need these lines
    key = cv2.waitKey()
    while chr(key) != 'q' and chr(key) != 'Q':
        key = cv2.waitKey()

    # we close all the opened OpenCV windows before exiting.
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()