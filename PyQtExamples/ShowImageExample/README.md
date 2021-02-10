# Show image example
This example shows how to show to load and how to show an image in the MainWindow.
It is supported by a custom class, that is in charge of converting an OpenCV
image into a Qt image to be shown. This class can be modified in the future,
in order to draw objects, lines, circles, etc, over the image.

Also, mouse events, clicks and mouse position can be captured in this widget also
so we can know in which pixel the user clicks. When we click the image, this example
prints in the terminal the pixel position pressed.
NOTE: The position returned is measured in the widget space, and not in the main window space.
Since we have two widgets in this case, if we click either the first pixel
of the first image, or the first pixel of the second image, we will obtain
the same value : (0,0). This means that, if we want to know which image
we clicked, we need to create an identifier for each widget (for instance,
when we click, we emit a signal that tells the pixel position, and the
ID of which image we clicked).

# Application screenshot
![app screenshot](/PyQtExamples/ShowImageExample/images/ShowImageExample.png)