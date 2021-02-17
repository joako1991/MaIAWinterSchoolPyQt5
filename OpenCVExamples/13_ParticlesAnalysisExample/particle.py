import numpy as np
import cv2

'''
This class holds all the requirements to compute the particles parameters, and
store them, so they can be requested later on.

The only parameters that have to be given are the class id, the image size, and the particle
pixel positions. Automatically, during construction, the program will compute
the particule parameters
'''
class Particle(object):
    def __init__(self, id, particle, img_size):
        '''
        Constructor.

        Args:
            id: Integer that represents the class identifier.
            particle: Array of the shape (2,N). Each element is a pixel that belongs
                to the binary region. N is the amount of pixels in the particle.
                (0,:) are the rows of all the pixels and (1,:) are the columns
        '''
        # We initialize all the variables
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

        # We initialize all the parameters
        self.compute_particle_params()

    def compute_particle_params(self):
        '''
        Compute all the particle parameters, and it stores them in this class
        '''
        # The parameters will be computed only if the particle have at least one pixel
        if self.particle_points.size:
            self.area = self.particle_points.shape[1]
            self.ratio = self.area / (self.image_size[0] * self.image_size[1])

            mass_center = self.get_particle_mass_center()
            self.mass_center_row = mass_center[0]
            self.mass_center_col = mass_center[1]

            self.enclosing_rect = self.get_enclosing_box()

            self.width = self.enclosing_rect[1][1] - self.enclosing_rect[0][1]
            self.height = self.enclosing_rect[1][0] - self.enclosing_rect[0][0]

            self.moment_0_0 = self.get_moment(0, 0, self.mass_center_row, self.mass_center_col)
            self.moment_1_0 = self.get_moment(1, 0, self.mass_center_row, self.mass_center_col)
            self.moment_0_1 = self.get_moment(0, 1, self.mass_center_row, self.mass_center_col)
            self.moment_1_1 = self.get_moment(1, 1, self.mass_center_row, self.mass_center_col)
            self.moment_2_0 = self.get_moment(2, 0, self.mass_center_row, self.mass_center_col)
            self.moment_0_2 = self.get_moment(0, 2, self.mass_center_row, self.mass_center_col)
            self.ellipse = self.get_ellipse_params(self.moment_0_0, self.moment_2_0, self.moment_0_2, self.moment_1_1)

            short_axis = self.ellipse[2]
            # We assign a tiny value to avoid the division by zero
            if short_axis == 0:
                short_axis = 0.01
            self.elongation = np.divide(self.ellipse[1], short_axis)**2

    def print_particle_params(self):
        '''
        Print all the parmeters of the particle
        '''
        print("Particle ID: {}".format(self.particle_id))
        print("Particle area: {}".format(self.area))
        print("Particle ratio: {}".format(self.ratio))

        print("Particle width: {}".format(self.width))
        print("Particle height: {}".format(self.height))

        print("Particle mass center row: {}".format(self.mass_center_row))
        print("Particle mass center columns: {}".format(self.mass_center_col))

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
        '''
        Compute the particle mass center (or gravity center). In order to compute
        the correct parameter, the particle points must have been provided previously.

        If the particle contains no points, the mass center will be set to
        (0,0)

        Returns:
            Tuple with the mass center given as (row,column). If the particle
            is empty, this tuple is (0,0).
        '''
        if self.particle_points.size:
            N = self.particle_points.shape[1]
            row_avg = np.sum(self.particle_points[0,:]) / float(N)
            col_avg = np.sum(self.particle_points[1,:]) / float(N)

            return (row_avg, col_avg)
        else:
            return (0,0)

    def get_enclosing_box(self):
        '''
        Determine the enclosing box of the particle. In order to detemine this
        box, 4 parameters are extracted: minimum row, minimum column, maximum row
        and maximum column.

        Returns:
            Array with two tuples. The first tuple contains the minimum
            row and column values, and the second one, the maximums.
        '''
        max_row = np.amax(self.particle_points[0,:])
        min_row = np.amin(self.particle_points[0,:])

        max_col = np.amax(self.particle_points[1,:])
        min_col = np.amin(self.particle_points[1,:])
        return [(min_row, min_col), (max_row, max_col)]

    def get_moment(self, p, q, center_row, center_col):
        '''
        Compute the central moment p,q of the particle.

        Args:
            p: order of the moment in the rows direction
            q: order of the moment in the columns direction
            center_row: Mass center in the rows direction
            center_col: Mass center in the columns direction

        Returns:
            Float value of the computed moment. If the particle size is zero,
            the moment is zero.
        '''
        if self.particle_points.size:
            # We remove the mass center from all the rows and from all the
            # columns
            rows = self.particle_points[0,:] - center_row
            cols = self.particle_points[1,:] - center_col

            # We power element-wise the previous variables
            rows_grid_p = np.power(rows, p)
            cols_grid_q = np.power(cols, q)

            # We multiply, element-wise, these two variables, and the result is a matrix.
            # Then, we sum all the elements of the resulting matrix.
            return np.sum(np.multiply(rows_grid_p, cols_grid_q))
        else:
            return 0

    def get_ellipse_params(self, m_0_0, m_2_0, m_0_2, m_1_1):
        '''
        Compute an equivalent ellipse from the central moments of the particle.
        This method is taken from the paper: Elliptical shape and size
        approximation of a particle contour. Ref: A Heyduk 2019 IOP Conf.
        Ser.: Earth Environ. Sci. 261 012013.

        Args:
            m_0_0: Central moment M00
            m_2_0: Central moment M20
            m_0_2: Central moment M02
            m_1_1: Central moment M11

        Returns:
            Ellipse parameters:
                1) Theta: Orientation of the major axis with respect to the
                    Horizontal axis, in radians.
                2) l: Major axis size
                3) w: Minor axis size
        '''
        # We check if the image has pixels
        if m_0_0:
            # We convert all the moments to float, to avoid problems of integer
            # divisions
            m_0_0 = float(m_0_0)
            m_2_0 = float(m_2_0)
            m_0_2 = float(m_0_2)
            m_1_1 = float(m_1_1)

            # We normalize all the moments, dividing them by the area (or m_0_0)
            a = m_2_0 / m_0_0
            # We multiply this factor by two, because in the
            # formula it always appears multiply by 2
            b = 2.0 * (m_1_1 / m_0_0)
            c = m_0_2 / m_0_0

            # We compute the different parameters as it is stated in the paper.
            # We invert C and A since they are taken in the XY system, and our
            # moments are computed in the IJ system
            theta = 0.5 * np.arctan2(b, (c - a))
            l = np.sqrt(8.0 * (a + c + np.sqrt((b**2) + ((a - c)**2))))
            w = np.sqrt(8.0 * (a + c - np.sqrt((b**2) + ((a - c)**2))))
            return [theta, l, w]
        else:
            return [0,0,0]