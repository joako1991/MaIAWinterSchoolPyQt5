import cv2
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
    # We print in the terminal the image shape: Rows, columns and channels
    print("Color image shape: {}".format(color_img.shape))

    # The images in OpenCV are coded as BGR, so the first channel is blue, the second
    # is green and the last one is red
    # We specify the window name
    gl_window_name = 'Red Channel'
    # We create a WINDOW_NORMAL in order to be able to resize it
    cv2.namedWindow(gl_window_name, cv2.WINDOW_NORMAL)
    # We show only the red channel. Since the image is a matrix (in this case, of the type NumPy array),
    # [:,:,2] means: All the rows, all the columns, and only the channel 2, which
    # corresponds to the red channel
    cv2.imshow(gl_window_name, color_img[:,:,2])

    # We do the same for the green channel
    gl_window_name = 'Green Channel'
    cv2.namedWindow(gl_window_name, cv2.WINDOW_NORMAL)
    # We show only the red channel. Since the image is a matrix (in this case, of the type NumPy array),
    # [:,:,1] means: All the rows, all the columns, and only the channel 1, which corresponds
    # to the green channel.
    cv2.imshow(gl_window_name, color_img[:,:,1])

    gl_window_name = 'Blue Channel'
    cv2.namedWindow(gl_window_name, cv2.WINDOW_NORMAL)
    # We show only the red channel. Since the image is a matrix (in this case, of the type NumPy array),
    # [:,:,0] means: All the rows, all the columns, and only the channel 0, which
    # corresponds to the blue channel
    cv2.imshow(gl_window_name, color_img[:,:,0])

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