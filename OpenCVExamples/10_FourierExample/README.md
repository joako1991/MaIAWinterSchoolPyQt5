# Filtrage in the Fourier domain example
In this example, we show how to apply linear filtering in the Fourier doamin.
Four filters are shown:
* Ideal low-pass filter: Only the central frequencies are kept.
* Ideal high-pass filter: Only the frequencies outside the center are kept.
* Ideal band-pass filter: Only the frequencies within a range are kept.
* Low-pass Gaussian filter: The frequencies around the center are kept,
    but also some frequencies that are between the blocked frequencies and
    the passing frequencies (known as transition band frequencies) are kept also, but
    with lower intensity. This is to avoid the artifacts present in the ideal case.

An important point is that, starting from the LP filter, the other ones can be
created easily:
- HP = 1 - LP
- BandPass = HP1 * LP2, where HP1 is a High-pass filter with a lower cut-off frequency than the LP filter LP2.
- RejectBand = 1 - BandPass

Since the property that the module of the FT is symmetric with respect to the
center, our filter have to be symmetric too.

# Application screenshot
![app screenshot](/OpenCVExamples/10_FourierExample/images/LPFilterFTExample.png)
![app screenshot](/OpenCVExamples/10_FourierExample/images/HPFilterFTExample.png)
![app screenshot](/OpenCVExamples/10_FourierExample/images/BandPassFiltered.png)
![app screenshot](/OpenCVExamples/10_FourierExample/images/LowPassGaussianFiltered.png)