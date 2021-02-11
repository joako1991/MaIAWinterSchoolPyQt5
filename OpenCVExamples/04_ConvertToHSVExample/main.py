import cv2
import os

root_dir = os.path.dirname(os.path.realpath(__file__))

def main():
    '''
    Main function. This example converts a normal BGR image into HSV space,
    and we show it.
    '''
    # As before, we insert the filepath of the image, and we open it as
    # a color image
    color_image_filepath = os.path.join(root_dir, 'images', 'Lenna.png')
    color_img = cv2.imread(color_image_filepath, cv2.IMREAD_COLOR | cv2.IMREAD_ANYDEPTH)
    # We show the color image shape: row, columns, channels
    print("Color image shape: {}".format(color_img.shape))

    # We convert from BGR to HSV using the flag: COLOR_BGR2HSV
    # IMPORTANT! In order to proceed to the convertion, the input image must be
    # a color image (i.e., it must have 3 channels), and it must be coded
    # in 8 bits. Any other type of image will make crash the program.
    hsv_image = cv2.cvtColor(color_img, cv2.COLOR_BGR2HSV)

    # We create a namedWindow, and we show the HSV image. In this example,
    # it is normal that the original color image and the corresponding HSV
    # image does not match. This is due to the imshow function EXPECTS A BGR
    # FORMAT IMAGE. If we pass the hsv image, since each channel represents
    # different image properties (instead of blue, green and red, we provide
    # hue, saturation and value), it is normal to think that the color will not
    # the original ones
    gl_window_name = 'HSV image'
    cv2.namedWindow(gl_window_name, cv2.WINDOW_NORMAL)
    cv2.imshow(gl_window_name, hsv_image)

    # We show the original image to constrast
    gl_window_name = 'Original color image'
    cv2.namedWindow(gl_window_name, cv2.WINDOW_NORMAL)
    cv2.imshow(gl_window_name, color_img)

    # These lines have to be always
    key = cv2.waitKey()
    while chr(key) != 'q' and chr(key) != 'Q':
        key = cv2.waitKey()

    cv2.destroyAllWindows()
    return

if __name__ == '__main__':
    main()