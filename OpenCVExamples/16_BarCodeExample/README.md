# Bars code detector example
This example shows how we can read and decode a bars code example. It implements
a class that contains all the required functionalities to read the bits in the
bars code, detect the orientation, check the presence of the start, central
and end codes, detect and decode the bits, and makes the error check.

Using this class, a few operations have to be done:
    - Load an image
    - Detect the orientation of the image (vertical or horizontal)
    - Extract a row that contains all the bars pixels
    - Pass this row to the decoder.

The decoder will automatically give you a string with the decoded value.

# Application screenshot
![app screenshot](/OpenCVExamples/16_BarCodeExample/images/AppHorizontal.png)
![app screenshot](/OpenCVExamples/16_BarCodeExample/images/AppVertical.png)