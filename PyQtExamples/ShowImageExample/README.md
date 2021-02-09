# Show image example
This example shows how to show to load and how to show an image in the MainWindow.
It is supported by a custom class, that is in charge of converting an OpenCV
image into a Qt image to be shown. This class can be modified in the future,
in order to draw objects, lines, circles, etc, over the image.

Also, mouse events, clicks and mouse position can be captured in this widget also
(it must be implemented), so we can know in which pixel the user clicks.

# Application screenshot
![app screenshot](/PyQtExamples/ShowImageExample/images/ShowImageExample.png)