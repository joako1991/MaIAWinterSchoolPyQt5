import cv2
import os

root_dir = os.path.dirname(os.path.realpath(__file__))

def main():
    '''
    This is the main function of the Python Script.
    It shows how to resize an image, using OpenCV. We do both cases, reducing
    the size with regard the original size, and increasing it.
    '''
    # As always, we specify the filepath of our image
    color_image_filepath = os.path.join(root_dir, 'images', 'Lenna.png')
    # We decide to treat it as a color image.
    color_img = cv2.imread(color_image_filepath, cv2.IMREAD_COLOR | cv2.IMREAD_ANYDEPTH)
    # We check if imread was able to find and open the image.
    if color_img is None:
        print("We couldn't load the image located at {}".format(color_image_filepath))
        return

    print("Color image shape: {}".format(color_img.shape))

    # reduced_dim is a tuple. The first element corresponds to the width (amount of columns)
    # that we want our final image to have. The second element is the height
    # (amount of rows) that we want to have in our output image. In this case,
    # we take the original size, and we divide it by two, but there are not any
    # restriction for the values given. We can set random values for the new image size if we want.
    # Nonetheless, we have to ensure that both numbers are positive, and
    # integers (they cannot be float value). That's why, after each division,
    # we convert the results into integers using the function int(.)
    reduced_dim = (int(color_img.shape[1] / 2.0), int(color_img.shape[0] / 2.0))
    # We resize the image. The first argument is the input image to be resized.
    # The second argument is the desired dimention, as a tuple with the
    # (width, height) parameters. Note that it is not in the order the shape property
    # gives us the image size. So, we cannot pass another image shape in this argument.
    # Moreover, the size does not include the amount of channels.
    # The third argument is the way the function estimates the pixels when we
    # expand an image. OpenCV provides several algorithms: INTER_LINEAR,
    # INTER_CUBIC, INTER_AREA, INTER_BITS, INTER_BITS2, INTER_LANCZOS4, INTER_MAX,
    # INTER_NEAREST.
    reduced_image = cv2.resize(color_img, reduced_dim, interpolation=cv2.INTER_)

    # Now we resize the image, but we increase its size. In this example, we
    # dupplicate each axis value. augmented_dim is the tuple with the final
    # image size. The first element is again the width, and the second one
    # is the height.
    augmented_dim = (int(color_img.shape[1] * 2.0), int(color_img.shape[0] * 2.0))
    # We resize the image. The arguments are exactly the same as in the case
    # of reducing the image size.
    enlarged_image = cv2.resize(color_img, augmented_dim, interpolation=cv2.INTER_LINEAR)

    # We show the smaller image
    color_window_name = 'Color image: Size reduced to the half'
    cv2.namedWindow(color_window_name, cv2.WINDOW_NORMAL)
    cv2.imshow(color_window_name, reduced_image)

    # We show the original image
    color_window_name = 'Color image'
    cv2.namedWindow(color_window_name, cv2.WINDOW_NORMAL)
    cv2.imshow(color_window_name, color_img)

    # We show the larger image
    color_window_name = 'Color image: Size dupplicated'
    cv2.namedWindow(color_window_name, cv2.WINDOW_NORMAL)
    cv2.imshow(color_window_name, enlarged_image)

    # We always need these lines
    key = cv2.waitKey()
    while chr(key) != 'q' and chr(key) != 'Q':
        key = cv2.waitKey()

    # we close all the opened OpenCV windows before exiting.
    cv2.destroyAllWindows()
    return

if __name__ == '__main__':
    main()