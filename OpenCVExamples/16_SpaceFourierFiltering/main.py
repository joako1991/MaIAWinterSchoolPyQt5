import cv2
import os

import numpy as np

root_dir = os.path.dirname(os.path.realpath(__file__))

def plot_fft(fft):
    '''
    We plot the magnitude of the FT.

    Args:
        fft: FT of the image
    '''
    # We compute the magnitude of the Fourier transform pixel-wise
    magnitude = np.absolute(fft)
    # Since the Fourier transform values might be really high, it is normal to
    # represent it in decibels (dB). Since this transformation passes the magnitude
    # through a logarithm function, we have to avoid the values between 0 and 1.
    magnitude[magnitude <= 1 ] = 1
    # We convert into dB scale
    log_ft = np.array(20.0 * np.log10(magnitude), dtype=np.uint8)

    # We show the magnitude plot
    win_name = 'Magnitude Fourier Transform in dB'
    cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)
    cv2.imshow(win_name, log_ft)

def get_lowpass_mask(image_shape, radius, center_rows, center_cols):
    '''
    Construct a disk-shaped low-pass filter mask.

    Args:
        image_shape: Amount of rows and columns of the image to be filtered
        radius: Disk radious

    Returns:
        Binary mask with value 1 in all the pixels where the passing frequencies
        are, and zero in the rest.
    '''
    # We create a mask of zeros with the same size as the input image.
    kernel = np.zeros(image_shape, dtype=np.float32)

    # Useful variables
    # Diameter
    length = 2 * radius

    # radius_2 = radius^2
    radius_2 = radius**2

    # We only check the pixels inside an square of side size = "length"
    for i in range(length):
        for j in range(length):
            # We compute the pixel coordinates where we would have to put 1
            # if that pixel falls inside the disk
            x = center_rows - (radius - i)
            y = center_cols - (radius - j)
            if (((radius - i)**2 + (radius - j)**2) < radius_2):
                kernel[x,y] = 1.0
    return kernel

def get_highpass_mask(image_shape, radius, center_rows, center_cols):
    '''
    Construct a disk-shaped high-pass filter mask.

    Args:
        image_shape: Amount of rows and columns of the image to be filtered
        radius: Disk radious

    Returns:
        Binary mask with value 1 in all the pixels where the passing frequencies
        are, and zero in the rest.
    '''
    return 1 - get_lowpass_mask(image_shape, radius, center_rows, center_cols)

def get_bandpass_mask(img_shape, min_freq, max_freq, center_rows, center_cols):
    '''
    Get the band-pass filter kernel in the Fourier space. This filter
    is a combination of a low pass filter and a high-pass filter, where the
    cut-off frequency of the LP filter is max_freq, and the cut-off frequency
    of the high-pass filter is min_freq.

    Args:
        image_shape: Amount of rows and columns of the image to be filtered
        min_freq: Disk radious of the high-pass filter part
        max_freq: Disk radious of the low-pass filter part

    Returns:
        Binary mask with value 1 in all the pixels where the passing frequencies
        are, and zero in the rest.
    '''
    # We compute a mask for the low pass filter
    low_pass_mask = get_lowpass_mask(img_shape, max_freq, center_rows, center_cols)
    # We compute a mask for the high pass filter
    high_pass_mask = get_highpass_mask(img_shape, min_freq, center_rows, center_cols)
    # We multiply both masks in order to get the final mask of the band-pass filter.
    return np.multiply(low_pass_mask, high_pass_mask)

def get_gaussian_low_pass(img_shape, sigma, center_rows, center_cols):
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

def filter_fourier_lowpass(img, radious):
    '''
    We filter an image in the Fourier domain applying an ideal low pass filter

    Args:
        img: Input image to be filtered
        radious: Radious of the disk-shaped filter used

    Returns:
        Filtered image in the spatial domain
    '''
    # We compute the Fourier transform of the image
    fourier_transform = np.fft.fft2(img)
    # We shift it to be to have the Optical Representation
    shifted_fft = np.fft.fftshift(fourier_transform)

    # We show the FT of the image
    plot_fft(shifted_fft)

    # We create our kernel function
    center_rows = int((shifted_fft.shape[0] / 2.0) + 0.5)
    center_cols = int((shifted_fft.shape[1] / 2.0) + 0.5)
    kernel = get_lowpass_mask(shifted_fft.shape[0:2], radious, center_rows, center_cols)

    # We show the kernel used
    win_name = 'Low pass filter Kernel'
    cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)
    # We multiply the kernel by 255 so that the 1 values will be plot as white
    cv2.imshow(win_name, np.array(255 * kernel, dtype=np.uint8))

    # We filter the image by multiplying the FT and the kernel
    filtered_ft = np.multiply(shifted_fft, kernel)

    # We shift back to the standard representation
    filtered_ft = np.fft.ifftshift(filtered_ft)

    # We apply the inverse fourier transform to get the final image
    restored_img = np.fft.ifft2(filtered_ft)

    # Since some numerical error might happen, the restored image can have
    # complex numbers with really tiny imaginary part, so we compute the absolute
    # value for each pixel to remove them and obtain a real image.
    restored_img = np.absolute(restored_img)

    return np.array(restored_img, dtype=np.uint8)

def filter_fourier_highpass(img, radious):
    '''
    We filter an image in the Fourier domain applying an ideal high-pass filter

    Args:
        img: Input image to be filtered
        radious: Radious of the disk-shaped filter used

    Returns:
        Filtered image in the spatial domain
    '''
    # We compute the Fourier transform of the image
    fourier_transform = np.fft.fft2(img)
    # We shift it to be to have the Optical Representation
    shifted_fft = np.fft.fftshift(fourier_transform)

    # We show the FT of the image
    plot_fft(shifted_fft)

    # We create our kernel function (compare with the kernel of the Low-pass filter)
    center_rows = int((shifted_fft.shape[0] / 2.0) + 0.5)
    center_cols = int((shifted_fft.shape[1] / 2.0) + 0.5)
    kernel = get_highpass_mask(shifted_fft.shape[0:2], radious, center_rows, center_cols)

    # We show the kernel used
    win_name = 'High pass filter Kernel'
    cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)
    # We multiply the kernel by 255 so that the 1 values will be plot as white
    cv2.imshow(win_name, np.array(255 * kernel, dtype=np.uint8))

    # We filter the image by multiplying the FT and the kernel
    filtered_ft = np.multiply(shifted_fft, kernel)

    # We shift back to the standard representation
    filtered_ft = np.fft.ifftshift(filtered_ft)

    # We apply the inverse fourier transform to get the final image
    restored_img = np.fft.ifft2(filtered_ft)

    # Since some numerical error might happen, the restored image can have
    # complex numbers with really tiny imaginary part, so we compute the absolute
    # value for each pixel to remove them and obtain a real image.
    restored_img = np.absolute(restored_img)

    return np.array(restored_img, dtype=np.uint8)

def filter_fourier_bandpass(img, low_freq, high_freq):
    '''
    We filter an image in the Fourier domain applying an ideal high-pass filter

    Args:
        img: Input image to be filtered
        radious: Radious of the disk-shaped filter used

    Returns:
        Filtered image in the spatial domain
    '''
    # We compute the Fourier transform of the image
    fourier_transform = np.fft.fft2(img)
    # We shift it to be to have the Optical Representation
    shifted_fft = np.fft.fftshift(fourier_transform)

    # We show the FT of the image
    plot_fft(shifted_fft)

    # We create our kernel function
    center_rows = int((shifted_fft.shape[0] / 2.0) + 0.5)
    center_cols = int((shifted_fft.shape[1] / 2.0) + 0.5)
    kernel = get_bandpass_mask(shifted_fft.shape[0:2], low_freq, high_freq, center_rows, center_cols)

    # We show the kernel used
    win_name = 'Band-pass filter Kernel'
    cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)
    # We multiply the kernel by 255 so that the 1 values will be plot as white
    cv2.imshow(win_name, np.array(255 * kernel, dtype=np.uint8))

    # We filter the image by multiplying the FT and the kernel
    filtered_ft = np.multiply(shifted_fft, kernel)

    # We shift back to the standard representation
    filtered_ft = np.fft.ifftshift(filtered_ft)

    # We apply the inverse fourier transform to get the final image
    restored_img = np.fft.ifft2(filtered_ft)

    # Since some numerical error might happen, the restored image can have
    # complex numbers with really tiny imaginary part, so we compute the absolute
    # value for each pixel to remove them and obtain a real image.
    restored_img = np.absolute(restored_img)

    return np.array(restored_img, dtype=np.uint8)

def filter_fourier_lowpass_gaussian(img, sigma):
    '''
    We filter an image in the Fourier domain applying a Gaussian low-pass filter

    Args:
        img: Input image to be filtered
        sigma: Standard deviation of the gaussian function

    Returns:
        Filtered image in the spatial domain.
    '''
    # We compute the Fourier transform of the image
    fourier_transform = np.fft.fft2(img)
    # We shift it to be to have the Optical Representation
    shifted_fft = np.fft.fftshift(fourier_transform)

    # We show the FT of the image
    plot_fft(shifted_fft)

    # We create our kernel function
    center_rows = 200
    center_cols = 200
    kernel = get_gaussian_low_pass(img.shape[0:2], sigma, center_rows, center_cols)

    # We show the kernel used
    win_name = 'Low-pass gaussian filter Kernel'
    cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)
    # We multiply the kernel by 255 so that the 1 values will be plot as white
    cv2.imshow(win_name, np.array(255 * kernel, dtype=np.uint8))

    # We filter the image by multiplying the FT and the kernel
    filtered_ft = np.multiply(shifted_fft, kernel)

    # We shift back to the standard representation
    filtered_ft = np.fft.ifftshift(filtered_ft)

    # We apply the inverse fourier transform to get the final image
    restored_img = np.fft.ifft2(filtered_ft)

    # Since some numerical error might happen, the restored image can have
    # complex numbers with really tiny imaginary part, so we compute the absolute
    # value for each pixel to remove them and obtain a real image.
    restored_img = np.absolute(restored_img)

    return np.array(restored_img, dtype=np.uint8)

def get_noise_centers():
    return

def main():
    # We define the image filepath we want to load
    color_image_filepath = os.path.join(root_dir, 'images', 'Space.png')
    # We load the image, and we pass the flag to load it as in gray-level mode.
    gray_img = cv2.imread(color_image_filepath, cv2.IMREAD_GRAYSCALE | cv2.IMREAD_ANYDEPTH)
    # We check if imread was able to find and open the image.
    if gray_img is None:
        print("We couldn't load the image located at {}".format(color_image_filepath))
        return

    # We filter the image with different kernels
    lowpass_gaussian = filter_fourier_lowpass_gaussian(gray_img, 20)

    # We show the loaded gray-level image
    gl_window_name = 'Gray-level image'
    # We create a namedWindow, with the flag cv2.WINDOW_NORMAL in order to be able
    # to resize the image as we want, with the mouse
    cv2.namedWindow(gl_window_name, cv2.WINDOW_NORMAL)
    # We show the image.
    cv2.imshow(gl_window_name, gray_img)

    # We show the low-pass gaussian filtered image
    gl_window_name = 'Low-pass gaussian filtered image'
    # We create a namedWindow, with the flag cv2.WINDOW_NORMAL in order to be able
    # to resize the image as we want, with the mouse
    cv2.namedWindow(gl_window_name, cv2.WINDOW_NORMAL)
    # We show the image.
    cv2.imshow(gl_window_name, lowpass_gaussian)

    # We always need these lines
    key = cv2.waitKey()
    while chr(key) != 'q' and chr(key) != 'Q':
        key = cv2.waitKey()

    # we close all the opened OpenCV windows before exiting.
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()