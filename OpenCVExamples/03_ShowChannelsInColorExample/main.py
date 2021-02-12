import cv2
import numpy as np
import os

root_dir = os.path.dirname(os.path.realpath(__file__))

def main():
    '''
    This is the main function of the program.
    It loads a color image, and it shows its channels as gray-level images
    separatedly. It also shows the original color image.
    '''
    # We specify the image filepath
    color_image_filepath = os.path.join(root_dir, 'images', 'Lenna.png')
    # We load the image as color
    color_img = cv2.imread(color_image_filepath, cv2.IMREAD_COLOR | cv2.IMREAD_ANYDEPTH)
    # We check if imread was able to find and open the image.
    if color_img is None:
        print("We couldn't load the image located at {}".format(color_image_filepath))
        return

    # We print in the terminal the image shape: Rows, columns and channels
    print("Color image shape: {}".format(color_img.shape))

    # we create an empty image, with only zeros, and the same size as the input image.
    red_image = np.zeros(color_img.shape, dtype=np.uint8)
    # We put only the red information on it
    red_image[:,:,2] = color_img[:,:,2]

    # The images in OpenCV are coded as BGR, so the first channel is blue, the second
    # is green and the last one is red
    # We specify the window name
    gl_window_name = 'Red Channel'
    # We create a WINDOW_NORMAL in order to be able to resize it
    cv2.namedWindow(gl_window_name, cv2.WINDOW_NORMAL)
    # We show the single color image
    cv2.imshow(gl_window_name, red_image)

    # we create an empty image, with only zeros, and the same size as the input image.
    green_image = np.zeros(color_img.shape, dtype=np.uint8)
    # We put only the green information on it
    green_image[:,:,1] = color_img[:,:,1]
    # We do the same for the green channel
    gl_window_name = 'Green Channel'
    cv2.namedWindow(gl_window_name, cv2.WINDOW_NORMAL)
    # We show the single color image
    cv2.imshow(gl_window_name, green_image)

    # we create an empty image, with only zeros, and the same size as the input image.
    blue_image = np.zeros(color_img.shape, dtype=np.uint8)
    # We put only the blue information on it
    blue_image[:,:,0] = color_img[:,:,0]
    gl_window_name = 'Blue Channel'
    cv2.namedWindow(gl_window_name, cv2.WINDOW_NORMAL)
    # We show the single color image
    cv2.imshow(gl_window_name, blue_image)

    # We show also the color image.
    gl_window_name = 'Color image'
    cv2.namedWindow(gl_window_name, cv2.WINDOW_NORMAL)
    cv2.imshow(gl_window_name, color_img)

    # They need to have these lines always we show images
    key = cv2.waitKey()
    while chr(key) != 'q' and chr(key) != 'Q':
        key = cv2.waitKey()

    # we close all the opened OpenCV windows before exiting.
    cv2.destroyAllWindows()
    return

if __name__ == '__main__':
    main()