# Message box example
This example shows how to create and show a message box.
A Meessage box is an adidtional window, smaller than the mainwindow, that
appears on top of it when we call its exec() function. This window starts in modal
mode, which means that we cannot touch anything from the mainwindow, until we close
it.
It is useful to show messages of confirmation, or important information regarding
problems, information, or errors in the program. For instance, for the given
parameters of the filter, it is not possible to apply the convolution of
an image. Or if we want to write an image in disk, and the file has the same
name as an existing one, we want the user to confirm that he will overwrite
the old file.

# Application screenshot
![app screenshot](/PyQtExamples/07_MessageBoxExample/images/MessageBoxExample.png)