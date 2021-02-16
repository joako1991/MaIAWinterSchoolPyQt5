import cv2
import os

import time

import numpy as np
from colors import hsv_label_colors

root_dir = os.path.dirname(os.path.realpath(__file__))

class Particle(object):
    def __init__(self, id, particle, img_size):
        self.particle_id = id
        self.particle_points = np.array(particle)
        self.image_size = img_size
        self.area = 0
        self.ratio = 0
        self.height = 0
        self.width = 0
        self.mass_center_row = 0
        self.mass_center_col = 0
        self.enclosing_rect = [(0,0), (0,0)]
        self.moment_0_0 = 0
        self.moment_1_0 = 0
        self.moment_0_1 = 0
        self.moment_1_1 = 0
        self.moment_2_0 = 0
        self.moment_0_2 = 0
        self.ellipse = [0,0,0]
        self.elongation = 0

        self.compute_particle_params()

    def compute_particle_params(self):
        if self.particle_points.size:
            self.area = self.particle_points.shape[1]
            self.ratio = self.area / (self.image_size[0] * self.image_size[1])

            mass_center = self.get_particle_mass_center()
            self.mass_center_row = mass_center[0]
            self.mass_center_col = mass_center[1]

            self.enclosing_rect = self.get_enclosing_box()

            self.width = self.enclosing_rect[1][1] - self.enclosing_rect[0][1]
            self.height = self.enclosing_rect[1][0] - self.enclosing_rect[0][0]

            self.moment_0_0 = self.get_moment(0, 0)
            self.moment_1_0 = self.get_moment(1, 0)
            self.moment_0_1 = self.get_moment(0, 1)
            self.moment_1_1 = self.get_moment(1, 1)
            self.moment_2_0 = self.get_moment(2, 0)
            self.moment_0_2 = self.get_moment(0, 2)
            self.gravity_center_row = self.moment_1_0 / self.moment_0_0
            self.gravity_center_col = self.moment_0_1 / self.moment_0_0
            self.ellipse = self.get_ellipse_params(self.moment_0_0, self.moment_2_0, self.moment_0_2, self.moment_1_1, self.gravity_center_row, self.gravity_center_col)

            short_axis = self.ellipse[2]
            # We assign a tiny value to avoid the division by zero
            if short_axis == 0:
                short_axis = 0.01
            self.elongation = np.divide(self.ellipse[1], short_axis)**2

    def print_particle_params(self):
        print("Particle ID: {}".format(self.particle_id))
        print("Particle area: {}".format(self.area))
        print("Particle ratio: {}".format(self.ratio))

        print("Particle width: {}".format(self.width))
        print("Particle height: {}".format(self.height))

        print("Particle mass center row: {}".format(self.mass_center_row))
        print("Particle mass center columns: {}".format(self.mass_center_col))

        print("Gravity center row: {}".format(self.gravity_center_row))
        print("Gravity center row: {}".format(self.gravity_center_col))
        print("Particle enclosing rectangle [(minRow, minCol), (maxRow, maxCol)]: {}".format(self.enclosing_rect))

        print("Particle moment 0,0: {}".format(self.moment_0_0))
        print("Particle moment 1,0: {}".format(self.moment_1_0))
        print("Particle moment 0,1: {}".format(self.moment_0_1))
        print("Particle moment 1,1: {}".format(self.moment_1_1))
        print("Particle moment 2,0: {}".format(self.moment_2_0))
        print("Particle moment 0,2: {}".format(self.moment_0_2))
        print("Ellipse params (theta, l, w): ({}, {}, {})".format(self.ellipse[0] * 180.0 / np.pi, self.ellipse[1], self.ellipse[2]))
        print("Elongation: {}".format(self.elongation))

    def get_particle_mass_center(self):
        if self.particle_points.size:
            N = self.particle_points.shape[1]
            row_avg = np.sum(self.particle_points[0,:]) / float(N)
            col_avg = np.sum(self.particle_points[1,:]) / float(N)

            return (row_avg, col_avg)
        else:
            return (0,0)

    def get_enclosing_box(self):
        max_row = np.amax(self.particle_points[0,:])
        min_row = np.amin(self.particle_points[0,:])

        max_col = np.amax(self.particle_points[1,:])
        min_col = np.amin(self.particle_points[1,:])
        return [(min_row, min_col), (max_row, max_col)]

    def get_moment(self, p, q):
        if self.particle_points.size:
            rows = self.particle_points[0,:]
            cols = self.particle_points[1,:]

            rows_grid_p = np.power(rows, p)
            cols_grid_q = np.power(cols, q)

            return np.sum(np.multiply(rows_grid_p, cols_grid_q))
        else:
            return 0

    def get_ellipse_params(self, m_0_0, m_2_0, m_0_2, m_1_1, gravity_center_row, gravity_center_col):
        if m_0_0:
            m_0_0 = float(m_0_0)
            m_2_0 = float(m_2_0)
            m_0_2 = float(m_0_2)
            m_1_1 = float(m_1_1)
            gravity_center_row = float(gravity_center_row)
            gravity_center_col = float(gravity_center_col)

            a = (m_2_0 / m_0_0) - np.power(gravity_center_row, 2)
            b = 2.0 * ((m_1_1 / m_0_0) - (gravity_center_row * gravity_center_col))
            c = (m_0_2 / m_0_0) - np.power(gravity_center_col, 2)
            theta = 0.5 * np.arctan2(b, (a - c))
            l = np.sqrt(8.0 * (a + c + np.sqrt((b**2) + ((a - c)**2))))
            w = np.sqrt(8.0 * (a + c - np.sqrt((b**2) + ((a - c)**2))))
            return [theta, l, w]
        else:
            return [0,0,0]

def create_color_image_from_labeled(labeled_img):
    output = np.zeros(labeled_img.shape + (3,), dtype=np.uint8)
    amount_labels = np.max(labeled_img) + 1

    amount_colors = len(hsv_label_colors)
    print("There are {} labels".format(amount_labels))

    for i in range(1, amount_labels):
        idx = i % amount_colors
        output[labeled_img == i] = hsv_label_colors[idx]

    return cv2.cvtColor(output, cv2.COLOR_HSV2BGR)

def convert_into_binary(labeled_img):
    output = np.zeros(labeled_img.shape, dtype=np.uint8)
    output[labeled_img != 0] = 1
    return output

def get_particles_params(labeled_img):
    particles = []
    amount_labels = np.amax(labeled_img) + 1
    np_img = np.array(labeled_img)

    for class_id in range(1, amount_labels):
        obj = np.array(np.where(np_img == class_id))
        my_particle = Particle(class_id, obj, np_img.shape)
        particles.append(my_particle)

    return particles

def show_particles_animation(particles):
    index = 1
    key = -1
    cv2.namedWindow('Animation', cv2.WINDOW_NORMAL)
    startAngle = 0
    endAngle = 360

    while key == -1 or (chr(key) != 'q' and chr(key) != 'Q'):
        part = particles[index]
        binary = np.zeros(part.image_size + (3,), dtype=np.uint8)
        binary[part.particle_points[0,:], part.particle_points[1,:]] = (255, 255, 255)

        diameter = 2.0 * np.sqrt(part.area / np.pi)
        axesLength = (int(part.ellipse[1]), int(part.ellipse[2]))

        center = (int(part.mass_center_col), int(part.mass_center_row))

        angle = part.ellipse[0] * 180.0 / np.pi
        binary = cv2.ellipse(binary, center, axesLength,
               angle, startAngle, endAngle, (0,255,0), thickness=1)

        cv2.imshow('Animation', binary)
        key = cv2.waitKey()

        index += 1
        if index >= len(particles):
            index = 1

        time.sleep(0.3)
    print("Exiting from while loop")
    cv2.destroyAllWindows()

def main():
    labeled_img_filepath = os.path.join(root_dir, 'images', 'labeled_metal_2.png')
    labeled_img = cv2.imread(labeled_img_filepath, cv2.IMREAD_GRAYSCALE | cv2.IMREAD_ANYDEPTH)
    # We check if imread was able to find and open the image.
    if labeled_img is None:
        print("We couldn't load the image located at {}".format(labeled_img_filepath))
        return

    binary = convert_into_binary(labeled_img)
    particles = get_particles_params(labeled_img)

    show_particles_animation(particles)

    filtered_image = np.zeros(binary.shape, dtype=np.uint8)

    min_angle = 30.0 * np.pi / 180.0
    max_angle = 70.0 * np.pi / 180.0
    min_area = 170
    max_area = 510
    min_elongation = 8
    max_elongation = 50
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