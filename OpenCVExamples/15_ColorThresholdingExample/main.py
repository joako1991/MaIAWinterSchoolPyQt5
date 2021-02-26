import cv2
import numpy as np
import os

root_dir = os.path.dirname(os.path.realpath(__file__))

def color_thresholding(img, min_hue, max_hue, min_sat=0, max_sat=100, min_val=0, max_val=100):
    '''
    Filter by color, using the HSV space. This function gives the option to
    put filtering criteria in each channel: Hue, Saturation and value. Only the
    hue minimum and maximum values are mandatory.

    Args:
        img: Input image, in BGR space.
        min_hue: Minimum hue value to filter. This value should be in the range [0, 360]
        max_hue: Maximum hue value to filter. This value should be in the range [0, 360]
        min_sat (optional): Minimum saturation value to filter. This value should be in the range [0, 100]
        max_sat (optional): Maximum saturation value to filter. This value should be in the range [0, 100]
        min_val (optional): Minimum value to filter. This value should be in the range [0, 100]
        max_val (optional): Maximum value to filter. This value should be in the range [0, 100]

    Returns:
        binary image with 1 placed in all the pixels that matches with the given criterias
        for Hue, Saturation and Value, and 0 in the rest.
    '''
    # Sanity check. We see if the input values are in the correct range.
    assert(min_hue >= 0 and max_hue <= 360)
    assert(min_sat >= 0 and max_sat <= 100)
    assert(min_val >= 0 and max_val <= 100)
    # We convert the input image into HSV space.
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # In OpenCV, Hue goes from 0 to 180, instead of 0 to 360, so we have to convert
    # our angle to this scale in order to compare them. Saturation and value channels
    # go from 0 until 255, so we convert them to be in the right range too.
    min_color = min_hue * (179.0 / 360.0)
    max_color = max_hue * (179.0 / 360.0)
    min_sat = min_sat * 255.0 / 100.0
    max_sat = max_sat * 255.0 / 100.0
    min_val = min_val * 255.0 / 100.0
    max_val = max_val * 255.0 / 100.0
    # We create a conditional image. This image will contain only two possible
    # values at each pixel: True or False. It will contain True only in the pixels
    # that matches with the criterias specified for the Hue, the saturation and the
    # value.
    conditional_img = (hsv_img[:,:,0] >= min_color) & (hsv_img[:,:,0] <= max_color) & (hsv_img[:,:,1] >= min_sat) & (hsv_img[:,:,1] <= max_sat) & (hsv_img[:,:,2] >= min_val) & (hsv_img[:,:,2] <= max_val)
    # In Python, when we cast Boolean values to integers, it assigns 0 to False
    # and 1 to True. As a consequence, the result of casting the conditional_img
    # will give us the mask we are looking for.
    binary_img = np.array(conditional_img, dtype=np.uint8)

    return binary_img

def filter_mask(binary_img, kernel_sizes):
    '''
    Apply some morphological operations to the mask, in order to filter little spots.
    This function will apply opening operations, with an ellipse shape. Each operation
    can have a different kernel size, based on the values given as arguments.

    Args:
        binary_img: Input binary mask to filter. This image must contain only two
            values: 0 and 1.
        kernel_sizes: List of kernel sizes value for the opening operation. If at
            any moment, the kernel size is zero or negative, we stop the filtering,
            and we return the current image.

    Returns:
        Filtered mask. This image will be binary, with the same size as the input image,
        with only two values, 0 and 1.
    '''
    # We set the initial value of the mask to be the input mask. This way, if both filtering
    # operations are skipped, the output will be equal to the input.
    filtered_mask = binary_img

    for kernel_size in kernel_sizes:
        # We check if we have to end the filtering operation.
        if kernel_size <= 0:
            break
        # We create the kernel, using the OpenCV function. For the shape, the options are:
        # cv2.MORPH_ELLIPSE --> Ellipse shape
        # cv2.MORPH_RECT --> Rectangular shape
        # cv2.MORPH_CROSS --> Cross shape
        # Then we specify the kernel shape, to be square (same amount of rows and columns)
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (kernel_size, kernel_size))
        # Then apply the opening operation, using the given kernel, to the input image filtered_mask.
        # We store the result in the same variable as the input image.
        filtered_mask = cv2.morphologyEx(filtered_mask, cv2.MORPH_OPEN, kernel, iterations=1)

    return filtered_mask

def get_color_filtered_image(img, mask):
    '''
    Filter the input image, and keep only the elements contained in the mask.
    The pixels positions where the mask is 1 will be kept in the original image.
    For example, if the pixel (2,4) is equal to 1 in the mask, then the pixel
    (2,4) from the original image will be copied in the output.
    If the pixel (10,1) is zero, then a zero is placed in the output image at
    the position (10,1).

    Args:
        img: Input image
        mask: Binary mask that will be used to filter the input image. This mask
            must contain only two gray-level values: 0 and 1.

    Returns:
        Filtered RGB image.
    '''
    # We create an image with the same shape as the input image. This variable
    # will be used to store the result.
    masked_img = np.zeros(img.shape, dtype=np.uint8)

    # We multiply, pixel-wise, each channel and the input mask. We store the result
    # of this multiplication into the corresponding channel of the output image.
    masked_img[:,:,0] = np.array(np.multiply(img[:,:,0], mask), dtype=np.uint8)
    masked_img[:,:,1] = np.array(np.multiply(img[:,:,1], mask), dtype=np.uint8)
    masked_img[:,:,2] = np.array(np.multiply(img[:,:,2], mask), dtype=np.uint8)

    return masked_img

def main():
    '''
    Main function of the script. This example will show how to filter an image
    based on color information, and morphological operators.
    '''
    filepath = os.path.join(root_dir, 'images', 'Balls.png')
    # We load the image, and we pass the flag to load it as in gray-level mode.
    img = cv2.imread(filepath, cv2.IMREAD_ANYCOLOR | cv2.IMREAD_ANYDEPTH)
    # We check if imread was able to find and open the image.
    if img is None:
        print("We couldn't load the image located at {}".format(filepath))
        return

    # We obtain a binary mask, where only the pixels that have a hue in the range
    # [35, 70] will have a value 1. This criteria corresponds to the yellow color
    binary_mask = color_thresholding(img, 35, 70)

    # We filter the mask three times:
    #   The first time, we apply a kernel of size 7,
    #   The second time, we apply a kernel of size 10.
    #   The third time, we apply a kernel of size 12.
    filtered_mask = filter_mask(binary_mask, [7, 10, 12])

    # We filter the color image, with the obtained mask.
    color_mask = get_color_filtered_image(img, filtered_mask)

    ########### We show the results #################
    ## We show the results
    win_name = 'Original image'
    cv2.namedWindow(win_name, cv2.WINDOW_NORMAL);
    cv2.imshow(win_name, img);

    win_name = 'Binary'
    cv2.namedWindow(win_name, cv2.WINDOW_NORMAL);
    cv2.imshow(win_name, np.array(255 * binary_mask, dtype=np.uint8));

    win_name = 'Binary filtered'
    cv2.namedWindow(win_name, cv2.WINDOW_NORMAL);
    cv2.imshow(win_name, np.array(255 * filtered_mask, dtype=np.uint8));

    win_name = 'Image filtered'
    cv2.namedWindow(win_name, cv2.WINDOW_NORMAL);
    cv2.imshow(win_name, color_mask);

    win_name = 'Substracted'
    cv2.namedWindow(win_name, cv2.WINDOW_NORMAL);
    cv2.imshow(win_name, img - color_mask);

    # We always need these lines
    key = cv2.waitKey()
    while chr(key) != 'q' and chr(key) != 'Q':
        key = cv2.waitKey()

    # we close all the opened OpenCV windows before exiting.
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()