import cv2
import os
import numpy as np

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
    # We create 
    binary = np.zeros(img.shape)
    binary[img > threshold] = 1
    return binary

def dilation(img, kernel):
    '''
    Apply the morphological operator DILATION with the given structuring element.
    This function takes the structuring element (kernel) and it slides it over all
    the image.

    It takes the piece of image that falls below the kernel, and it makes a
    pixel-wise multiplication, which gives us another matrix.
    Then, the elements result of that multiplication are summed all together
    and if the result of that sum if higher or equal to 1, we assign the value 1
    to the central pixel. If this sum gives zero, we assign zero.

    The reference element is taken as the central element of the kernel: If the
    kernel size is MxN, the central pixel is: (M / 2, N / 2)

    Args:
        img: Binary input image (The only possible values are 0 and 1).
        kernel: Structuring element. It is given in the form of a matrix, with
            1s in the positions that belong to the structuring element, and
            zeros in the rest of elements of the matrix.

    Returns:
        Binary image after applying dilation.    
    '''
    # We check that both sizes (rows and columns) of the kernel are odd numbers
    assert(kernel.shape[0] % 2 and kernel.shape[1] % 2)

    # We pad the image with zeros the input image, so the output image has
    # the same size as the input after this operation
    rows_to_add = int((kernel.shape[0] - 1) / 2.0)
    cols_to_add = int((kernel.shape[1] - 1) / 2.0)
    padded_img = np.pad(img, ((rows_to_add,rows_to_add), (cols_to_add,cols_to_add)), 'constant')

    # We create an empty output image, filled with zeros
    output = np.zeros(img.shape)

    # We travel over all the output image (pixel by pixel).
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            # We compute the range of rows of the input image involved for the pixel (i,j)
            start_row = i
            end_row = i + kernel.shape[0]

            # We compute the range of columns of the input image involved for the pixel (i,j)
            start_col = j
            end_col = j + kernel.shape[1]

            # We multiply the kernel with the piece of image, element-wise, and
            # we sum all the elements, result of that multiplication.
            condition = np.sum(np.multiply(kernel, padded_img[start_row:end_row, start_col:end_col]))
            # If the result of the previous operation is higher than 1, we assign
            # 1 to the pixel (i,j). If not, do not do anything (the output image
            # is already filled with zeros)
            if condition >= 1:
                output[i,j] = 1
    return output

def erosion(img, kernel):
    '''
    Apply the morphological operator EROSION with the given structuring element.
    This function takes the structuring element (kernel) and it slides it over all
    the image.

    It takes the piece of image that falls below the kernel, and it makes a
    pixel-wise multiplication, which gives us another matrix.
    Then, all the elements result of that multiplication are multiplied together
    and if the result is 1, we assign the value 1 to the central pixel.
    If this multiplication gives zero, we assign zero.

    The reference element is taken as the central element of the kernel: If the
    kernel size is MxN, the central pixel is: (M / 2, N / 2)

    Args:
        img: Binary input image (The only possible values are 0 and 1).
        kernel: Structuring element. It is given in the form of a matrix, with
            1s in the positions that belong to the structuring element, and
            zeros in the rest of elements of the matrix.
            IMPORTANT: The size of the kernel must be an odd number (3, 5, 7, etc).

    Returns:
        Binary image after applying erosion.
    '''
    # We check that both sizes (rows and columns) of the kernel are odd numbers
    assert(kernel.shape[0] % 2 and kernel.shape[1] % 2)

    # We pad the image with zeros the input image, so the output image has
    # the same size as the input after this operation
    rows_to_add = int((kernel.shape[0] - 1) / 2.0)
    cols_to_add = int((kernel.shape[1] - 1) / 2.0)
    padded_img = np.pad(img, ((rows_to_add,rows_to_add), (cols_to_add,cols_to_add)), 'constant')

    # We create an empty output image, filled with zeros
    output = np.zeros(img.shape)

    # We travel over all the output image (pixel by pixel).
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            # We compute the range of rows of the input image involved for the pixel (i,j)
            start_row = i
            end_row = i + kernel.shape[0]

            # We compute the range of columns of the input image involved for the pixel (i,j)
            start_col = j
            end_col = j + kernel.shape[1]

            # We multiply the kernel with the piece of image, element-wise, and
            # we multiply all the elements, result of that multiplication.
            condition = np.prod(np.multiply(kernel, padded_img[start_row:end_row, start_col:end_col]))

            # If the result of the previous operation is equal to 1, we assign
            # 1 to the pixel (i,j). If not, do not do anything (the output image
            # is already filled with zeros)
            if condition == 1:
                output[i,j] = 1

    return output

def opening(img, kernel):
    '''
    Apply the opening operation to the image. This operation consists of applying
    sequentially, the erosion operation and the dilation operation. Both
    morphological operations are applied using the same structuring element.

    Args:
        img: Binary input image (The only possible values are 0 and 1).
        kernel: Structuring element. It is given in the form of a matrix, with
            1s in the positions that belong to the structuring element, and
            zeros in the rest of elements of the matrix.
            IMPORTANT: The size of the kernel must be an odd number (3, 5, 7, etc).

    Returns:
        Binary image after applying opening.
    '''
    output = erosion(img,kernel)
    output = dilation(output,kernel)
    return output

def closing(img, kernel):
    '''
    Apply the closing operation to the image. This operation consists of applying
    sequentially, the dilation operation and the erosion operation. Both
    morphological operations are applied using the same structuring element.

    Args:
        img: Binary input image (The only possible values are 0 and 1).
        kernel: Structuring element. It is given in the form of a matrix, with
            1s in the positions that belong to the structuring element, and
            zeros in the rest of elements of the matrix.
            IMPORTANT: The size of the kernel must be an odd number (3, 5, 7, etc).

    Returns:
        Binary image after applying opening.
    '''
    output = dilation(img,kernel)
    output = erosion(output,kernel)
    return output

def main():
    # We define the image filepath we want to load.
    color_image_filepath = os.path.join(root_dir, 'images', 'metal.png')
    # color_image_filepath = os.path.join(root_dir, 'images', 'j.png')
    # color_image_filepath = os.path.join(root_dir, 'images', 'tachedJ.png')
    # color_image_filepath = os.path.join(root_dir, 'images', 'holesJ.png')

    # We load the image, and we pass the flag to load it as in gray-level mode.
    gray_img = cv2.imread(color_image_filepath, cv2.IMREAD_GRAYSCALE | cv2.IMREAD_ANYDEPTH)
    # We check if imread was able to find and open the image.
    if gray_img is None:
        print("We couldn't load the image located at {}".format(color_image_filepath))
        return

    # We threshold the image, in order to have a binary image
    binary = threshold_image(gray_img, 180)
    # We apply the 4 morphological operators with a matrix of 5x5, filled with ones.
    dilated_img = dilation(binary, np.ones((5,5)))
    eroded_img = erosion(binary, np.ones((5,5)))
    opened_img = opening(binary, np.ones((5,5)))
    closed_img = closing(binary, np.ones((5,5)))

    ######################## We show the results ########################
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
    cv2.imshow(gl_window_name, 255 * binary)

    # We show the erosed image
    gl_window_name = 'Eroded image'
    # We create a namedWindow, with the flag cv2.WINDOW_NORMAL in order to be able
    # to resize the image as we want, with the mouse
    cv2.namedWindow(gl_window_name, cv2.WINDOW_NORMAL)
    # We show the image.
    cv2.imshow(gl_window_name, 255 * eroded_img)

    # We show the dilated image
    gl_window_name = 'Dilated image'
    # We create a namedWindow, with the flag cv2.WINDOW_NORMAL in order to be able
    # to resize the image as we want, with the mouse
    cv2.namedWindow(gl_window_name, cv2.WINDOW_NORMAL)
    # We show the image.
    cv2.imshow(gl_window_name, 255 * dilated_img)

    # We show the Opened image
    gl_window_name = 'Opened image'
    # We create a namedWindow, with the flag cv2.WINDOW_NORMAL in order to be able
    # to resize the image as we want, with the mouse
    cv2.namedWindow(gl_window_name, cv2.WINDOW_NORMAL)
    # We show the image.
    cv2.imshow(gl_window_name, 255 * opened_img)

    # We show the Closed image
    gl_window_name = 'Closed image'
    # We create a namedWindow, with the flag cv2.WINDOW_NORMAL in order to be able
    # to resize the image as we want, with the mouse
    cv2.namedWindow(gl_window_name, cv2.WINDOW_NORMAL)
    # We show the image.
    cv2.imshow(gl_window_name, 255 * closed_img)

    # We always need these lines
    key = cv2.waitKey()
    while chr(key) != 'q' and chr(key) != 'Q':
        key = cv2.waitKey()

    # we close all the opened OpenCV windows before exiting.
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()