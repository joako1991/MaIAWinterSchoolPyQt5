import cv2
import os

root_dir = os.path.dirname(os.path.realpath(__file__))

def main():
    '''
    This is the main function of the program.
    This example opens two images, a gray-scale image, and a color image, it
    prints the corresponding shapes (size and amount of channels), and it shows
    them. This is the most basic examples we can do with OpenCV.
    '''
    # We create variables with the full path of the images. In the rest of the
    # program, we just the variables. This is a good technique, so we do not
    # have to look further in the code for these paths if the filepath changes,
    # or if we want to open other images. Also, if we want to use it several
    # times, and then it changes, we do not have to look for each time we used
    # the old path in the middle of the code.
    color_image_filepath = os.path.join(root_dir, 'images', 'Lenna.png')

    # We open the two images using the function cv2.imread. Notiche that we
    # we only changed the flags we pass as second argument:
    #   *) In the first case, we have the flag IMREAD_GRAYSCALE, so we inform OpenCV
    #       we want to open the image as gray-scale. If the passed image is color,
    #       this function automatically converts it into grayscale.
    #   *) In the second case, we pass the flag IMREAD_COLOR. This means, that
    #       we want to consider the opened image as color. If the file is a
    #       gray scale image, and we pass the color flag, it will replicate the same
    #       the gray-scale matrix 3 times, one per channel, but the result image
    #       will look as gray.
    # In both cases, we pass the IMREAD_ANYDEPTH flag, which allows us to support
    # even images coded in 16-bits, or more.
    gray_img = cv2.imread(color_image_filepath, cv2.IMREAD_GRAYSCALE | cv2.IMREAD_ANYDEPTH)
    if gray_img is None:
        print("We couldn't load the image located at {}".format(color_image_filepath))
        return

    color_img = cv2.imread(color_image_filepath, cv2.IMREAD_COLOR | cv2.IMREAD_ANYDEPTH)
    if color_img is None:
        print("We couldn't load the image located at {}".format(color_image_filepath))
        return

    # We print in the terminal both images shape. The gray level image, since it
    # has 1 channel, the shape property contains 2 elements: rows and columns.
    # The color image contains 3 numbers in its shape property: Row, columns,
    # and channels
    print("Gray-level image shape: {}".format(gray_img.shape))
    print("Color image shape: {}".format(color_img.shape))

    # In order to show the images, we need to specify the window name. If
    # we call imshow with different names, it will show two windows. If we use
    # the same window name for both cases, both images will be shown in the same
    # window, but the second print will erase the first one, so we will only see
    # the second image all the time.
    gl_window_name = 'Gray-level image'
    # We create a namedWindow, with the flag cv2.WINDOW_NORMAL in order to be able
    # to resize the image as we want, with the mouse
    cv2.namedWindow(gl_window_name, cv2.WINDOW_NORMAL)
    # We show the image.
    cv2.imshow(gl_window_name, gray_img)

    # Here we do the same for the corresponding color image.
    color_window_name = 'Color image'
    cv2.namedWindow(color_window_name, cv2.WINDOW_NORMAL)
    cv2.imshow(color_window_name, color_img)

    # This function is really important. If we do not write it, the shown window with
    # the image will block, and it will not respond to anything we do. We call
    # cv2.waitKey() after we called all the cv2.imshow functions we want.
    # waitKey blocks the execution until we press a key in the keyboard
    key = cv2.waitKey()
    # This is not necessary. It will check if the entered key with the keyboard
    # is either q or Q. If not, it waits again for another entered key. If the
    # entered key is q or Q, the while loop finishes
    while chr(key) != 'q' and chr(key) != 'Q':
        key = cv2.waitKey()

    # we close all the opened OpenCV windows before exiting.
    cv2.destroyAllWindows()
    return

if __name__ == '__main__':
    main()