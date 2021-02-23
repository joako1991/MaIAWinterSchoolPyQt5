# Image Processing - Introduction to Image Processing - IUT
This repository contains several examples of code in Python, for the libraries OpenCV and PyQt.
OpenCV will be useful to open images, treat them, change them from one color space to another one, show them, and more.
PyQt is a framework that allow us, in a very structured way, to create user interfaces.
We can show images, create buttons, lists, menus, tabs, explore the disk looking for a folder,
slide bars, spin boxes, check boxes, grab the clicks from the mouse, and much more.

The two main folders are:
* OpenCVExamples: Several basic operations using only with OpenCV. Each sub-folder
    contains a single examples of code that makes the work.
* PyQtExamples: Each sub-folder contains a single example with a specific purpose.
    In all the cases, we have the basic mainwindow class, and a specific application:
        A button, a label, an show image, slide bar, spinbox.

Each example contains a little readme examplaing how it works,
with a screenshot of the application you should see. This will help you to
know quickly if that example works for you or not.

The main idea of this repository is give you the most basic templates you can
have for each application, and your project will make use of several of them.

In order to execute any of these examples, we move to the folder that holds the
example we want, and we execute: ```python3 ./main.py```

# Requirements
* python3 -m pip install pip --upgrade
* python3 -m pip install opencv-python
* python3 -m pip install pyqt5==5.12
* python3 -m pip install numpy
* python3 -m pip install matplotlib
