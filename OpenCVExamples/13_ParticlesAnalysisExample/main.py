import cv2
import os

import numpy as np
from colors import hsv_label_colors
from particle import Particle

root_dir = os.path.dirname(os.path.realpath(__file__))

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

def convert_into_binary(labeled_img):
    '''
    We convert the labeled image into binary again. In this case, any value
    that is not zero, have to be set to 1.

    Args:
        labeled: Image labeled using the connected components algorithm. Each
            pixel contains an integer number that identifies the class to which
            it belongs to. 0 is the background always.

    Returns:
        Binary image, with only 0s and 1s.
    '''
    # We create an image with zeros only, and with the same size as the input image.
    output = np.zeros(labeled_img.shape, dtype=np.uint8)
    # We set to 1 all the pixels that are not background.
    output[labeled_img != 0] = 1
    return output

def get_particles_params(labeled_img):
    '''
    Create particle objects for each binary object in the image. Each object
    contains the parameters of the given particle.

    Args:
        labeled: Image labeled using the connected components algorithm. Each
            pixel contains an integer number that identifies the class to which
            it belongs to. 0 is always the background.

    Returns:
        Array with as many particles as classes in the labeled image. Each
        element in this array contains all the computed parameters of the particle.
    '''
    # We create an empty list where we will store all the parameters.
    particles = []
    # We store in the variable the amount of labels present in the image.
    amount_labels = np.amax(labeled_img) + 1
    # We convert the image to a numpy array, to be sure that we count with the
    # indexing property of numpy arrays
    np_img = np.array(labeled_img)

    # For each class, we extract which pixels belongs to the given class, and
    # we create a particle object, that we store in our list called "particles"
    for class_id in range(1, amount_labels):
        obj = np.array(np.where(np_img == class_id))
        my_particle = Particle(class_id, obj, np_img.shape)
        particles.append(my_particle)

    return particles

def show_particles_animation(particles):
    '''
    Animation that shows particle by particle, with the equivalent ellipse
    corresponding to that particle. Pressing any key will make the animation
    to swtich to the next particle. When all the particles have been shown,
    it restarts showing the first one. If we press Q or q, the animation exits.

    Args:
        particles: Array with all the particles computed in the image.
    '''
    index = 1
    key = -1
    # We create a named window where we will show the animation
    cv2.namedWindow('Animation', cv2.WINDOW_NORMAL)
    # These are the angles used to plot the ellipse. Since we want the entire ellipse
    # to be shown, we go from 0 until 360 degrees.
    startAngle = 0
    endAngle = 360

    # We repeat the loop while we do not press any key, or until the entered key is q or Q.
    while key == -1 or (chr(key) != 'q' and chr(key) != 'Q'):
        # We get the particle that corresponds to the index i
        part = particles[index]
        # WE create an empty image, filled with zeros, and with 3 channels
        binary = np.zeros(part.image_size + (3,), dtype=np.uint8)
        # We set a white color to all the points that belong to this particle.
        binary[part.particle_points[0,:], part.particle_points[1,:]] = (255, 255, 255)

        # diameter = 2.0 * np.sqrt(part.area / np.pi)
        # We create a tuple with the major and minor axis of the ellipse. Note
        # that both values have to be integer values.
        axesLength = (int(part.ellipse[1] / 2.0), int(part.ellipse[2] / 2.0))

        # We create a tuple with the coordinates of the center of the ellipse,
        # in XY system (not in ij).Note that both values have to be integer values.
        center = (int(part.mass_center_col), int(part.mass_center_row))

        # We create a variable with the angle of the ellipse, in degrees.
        angle = part.ellipse[0] * 180.0 / np.pi
        # We plot the ellipse in the binary image, centered in "center", with the
        # major and minor axis given by "axesLength", rotated "angle" degrees,
        # from 0 until 360 degrees.
        binary = cv2.ellipse(binary, center, axesLength,
               angle, startAngle, endAngle, (0,255,0), thickness=1)

        # We show the image
        cv2.imshow('Animation', binary)
        # We see the user response
        key = cv2.waitKey()

        index += 1
        if index >= len(particles):
            index = 1

    cv2.destroyAllWindows()

def main():
    '''
    Main function of this Python script.

    This example loads a labeled image of several liquid metal particles. Then,
    we compute several parameters of these particles, and we are able to filter
    them, based on certain criterias over those parameters.
    '''
    # We define our image filepath
    labeled_img_filepath = os.path.join(root_dir, 'images', 'labeled_metal_2.png')
    # We load our image as a grayscale image
    labeled_img = cv2.imread(labeled_img_filepath, cv2.IMREAD_GRAYSCALE | cv2.IMREAD_ANYDEPTH)
    # We check if imread was able to find and open the image.
    if labeled_img is None:
        print("We couldn't load the image located at {}".format(labeled_img_filepath))
        return

    # We convert our image into binary to show it.
    binary = convert_into_binary(labeled_img)
    # We split the image into Particles, and we compute the different parameters of them
    particles = get_particles_params(labeled_img)

    # # We show an animation of the particles
    # show_particles_animation(particles)

    # FILTERING: We create a binary image in which we will add only the particles
    # that comply with certain criterias
    filtered_image = np.zeros(binary.shape, dtype=np.uint8)

    # We define some variables for the criterias:
    ## Orientations: min and max
    min_angle = 30.0 * np.pi / 180.0
    max_angle = 70.0 * np.pi / 180.0
    # Area: Min and max
    min_area = 170
    max_area = 510
    # Elongation: min and max
    min_elongation = 8
    max_elongation = 50

    # We search in all the particles, and we check if they comply with the different criterias
    for part in particles:
        # # Filter 1: Filter by area
        # if part.area < max_area and part.area > min_area:
        #     filtered_image[part.particle_points[0,:], part.particle_points[1,:]] = 1
        #     part.print_particle_params()

        # # Filter 2: Filter by elongation
        # if part.elongation < max_elongation and part.elongation > min_elongation:
        #     filtered_image[part.particle_points[0,:], part.particle_points[1,:]] = 1
        #     part.print_particle_params()

        # # Filter 3: Filter by elongation and area
        # if part.elongation < max_elongation and part.elongation > min_elongation and part.area < 3000 and part.area > 100:
        #     filtered_image[part.particle_points[0,:], part.particle_points[1,:]] = 1
        #     part.print_particle_params()

        # Filter 4: Elongation, orientation and area
        if part.elongation > 10 and part.ellipse[0] > min_angle and part.ellipse[0] < max_angle and part.area < 1700:
            filtered_image[part.particle_points[0,:], part.particle_points[1,:]] = 1
            part.print_particle_params()

    ################### We show the original binary image, and the filtered image ##################
    gl_window_name = 'Binary image'
    cv2.namedWindow(gl_window_name, cv2.WINDOW_NORMAL)
    cv2.imshow(gl_window_name, 255 * binary)

    gl_window_name = 'Filtered image'
    cv2.namedWindow(gl_window_name, cv2.WINDOW_NORMAL)
    cv2.imshow(gl_window_name, 255 * filtered_image)

    # These lines we need them always
    key = cv2.waitKey()
    while chr(key) != 'q' and chr(key) != 'Q':
        key = cv2.waitKey()

    cv2.destroyAllWindows()
    return

if __name__ == '__main__':
    main()