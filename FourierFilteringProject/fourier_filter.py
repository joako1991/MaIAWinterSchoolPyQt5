import numpy as np
import copy

class FourierFilter(object):
    def __init__(self):
        self.original_fourier_transform = np.array([])
        self.current_fourier_transform = np.array([])
        self.filter_centers_list = []
        self.filter_radius_list = []
        self.filter_type_list = []
        self.cumulative_kernel = None

        self.LOW_PASS_FILTER = 1
        self.HIGH_PASS_FILTER = 2

    def update_image(self, img):
        if img.size:
            self.reset_filtering()
            self.original_fourier_transform = np.fft.fftshift(np.fft.fft2(img))
            self.current_fourier_transform = copy.deepcopy(self.original_fourier_transform)
            self.cumulative_kernel = np.ones(self.original_fourier_transform.shape)
            print("Image_updated")
        else:
            print("Empty image. Avoiding fourier image update")

    def reset_filtering(self):
        self.filter_centers_list.clear()
        self.filter_radius_list.clear()
        self.filter_type_list.clear()
        if self.original_fourier_transform.size:
            self.current_fourier_transform = copy.deepcopy(self.original_fourier_transform)
            self.cumulative_kernel = np.ones(self.original_fourier_transform.shape)
        else:
            self.current_fourier_transform = np.array([])
            self.cumulative_kernel = np.array([])

    def get_gaussian_low_pass(self, img_shape, sigma, center_rows, center_cols):
        sigma_2 = sigma**2

        rows = np.arange(img_shape[0])
        cols = np.arange(img_shape[1])

        xx, yy = np.meshgrid(rows, cols, indexing='ij', sparse=True)
        xx = xx - center_rows
        yy = yy - center_cols

        exponent = (np.power(xx, 2) + np.power(yy, 2)) / (2 * sigma_2)
        kernel = np.exp((-1) * exponent)
        max_val = np.max(kernel)

        return np.array(kernel / max_val, dtype=np.float32)

    def get_gaussian_high_pass(self, img_shape, sigma, center_rows, center_cols):
        return 1.0 - self.get_gaussian_low_pass(img_shape, sigma, center_rows, center_cols)

    def create_filter_mask(self, img_shape):
        kernel = np.ones(img_shape[0:2])
        for i in range(len(self.filter_centers_list)):
            center = self.filter_centers_list[i]
            radius = self.filter_radius_list[i]
            filter_type = self.filter_type_list[i]

            if filter_type == self.HIGH_PASS_FILTER:
                local = 1.0 - self.get_gaussian_low_pass(img_shape, radius, center[0], center[1])
            elif filter_type == self.LOW_PASS_FILTER:
                local = self.get_gaussian_low_pass(img_shape, radius, center[0], center[1])
            else:
                print("ERROR!!! The specified kernel type is not valid: {}".format(filter_type))
                break

            kernel = np.multiply(kernel, local)

        return kernel

    def get_image_fft(self):
        magnitude = np.absolute(self.current_fourier_transform)
        magnitude[magnitude <= 1 ] = 1
        log_ft = np.array(20.0 * np.log10(magnitude), dtype=np.uint8)
        return log_ft

    def add_filter(self, filter_type, radius, row, column):
        if self.original_fourier_transform.size:
            local = np.ones(self.original_fourier_transform.shape)
            if filter_type == self.HIGH_PASS_FILTER:
                local = 1.0 - self.get_gaussian_low_pass(self.current_fourier_transform.shape, radius, row, column)
            elif filter_type == self.LOW_PASS_FILTER:
                local = self.get_gaussian_low_pass(self.current_fourier_transform.shape, radius, row, column)
            else:
                print("Not supported filter. Received {}".format(filter_type))
                return

            # We add the new filter to the list
            self.filter_centers_list.append([row, column])
            self.filter_radius_list.append(radius)
            self.filter_type_list.append(filter_type)

            self.cumulative_kernel = np.multiply(self.cumulative_kernel, local)
            self.current_fourier_transform = np.multiply(self.original_fourier_transform, self.cumulative_kernel)

    def remove_last_filter(self):
        if self.original_fourier_transform.size and len(self.filter_centers_list):
            try:
                self.filter_centers_list.pop()
                self.filter_radius_list.pop()
                self.filter_type_list.pop()
                self.cumulative_kernel = self.create_filter_mask(self.current_fourier_transform.shape)
                self.current_fourier_transform = np.multiply(self.original_fourier_transform, self.cumulative_kernel)
                print("I removed the previous kernel")
            except ValueError:
                print("I couldn't find the specified filter position")
                pass