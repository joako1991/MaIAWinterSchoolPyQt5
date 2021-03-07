from PyQt5.QtWidgets import \
    QScrollArea, \
    QHBoxLayout, \
    QMainWindow, \
    QVBoxLayout, \
    QWidget

from PyQt5.QtCore import \
    QTimer

import matplotlib.pyplot as plt
import numpy as np
import cv2

from image_widget import ImageWidget

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        '''
        Constructor. In this function, we create all the variables we will use
        in the code. If we cannot assign any value yet, we assign None. This way,
        from the beginning of the class, we know all the variables that belongs
        to the class. If not, we have to read all the code in order to know, and
        if we read the variable and it has not been created yet, the program will
        crash.
        '''
        super(MainWindow, self).__init__(parent)

        self.right_layout = QVBoxLayout()
        self.left_layout = QVBoxLayout()
        self.main_layout = QHBoxLayout()

        self.factor = 1.0
        self.constant_sign = 1.0
        self.timer = None

        self.initialize_widget()
        self.setWindowTitle("This is my template example")

    def initialize_widget(self):
        '''
        Function that initializes the MainWindow. It will add all the widgets
        attached to it. Each widget might have some initializations to do also,
        so those initializations must be done before exiting this function.

        The recommended way to do it is that each widget to attach will be added
        by calling a method that will do all the required initialization for that
        widget.
        '''
        ## Here you start initializing your widgets
        self.add_image()

        # Add the widgets that we want to add to the MainWindow must be added
        # before this line
        self.set_main_window_layouts()

    def set_main_window_layouts(self):
        '''
        Set the MainWindow Layout. We change the default MainWindow widget
        to be in two parts: Left and Right. So we can, for instance, show
        images in the left, and have control buttons to the right.

        For that, two layouts exists in the program: self.left_layout and
        self.right_layout.
        '''
        # We create scroll area to allows to slide the window, when the screen
        # size is not enough
        left_scroll = QScrollArea()
        right_scroll = QScrollArea()

        left_scroll.setWidgetResizable(True)
        right_scroll.setWidgetResizable(True)

        # The MainWindow is splitted into two areas, left and right, each of them
        # with the corresponding layouts
        left_widget = QWidget()
        right_widget = QWidget()
        main_widget = QWidget()

        left_widget.setLayout(self.left_layout)
        left_scroll.setWidget(left_widget)
        self.right_layout.addStretch(1)
        right_widget.setLayout(self.right_layout)
        right_scroll.setWidget(right_widget)

        self.main_layout.addWidget(left_scroll)
        self.main_layout.addWidget(right_scroll)
        main_widget.setLayout(self.main_layout)

        self.setCentralWidget(main_widget)

    def create_matplotlib_plot_img(self, delta_factor):
        '''
        This function creates a 2D curve plot to show as an image in our MainWindow.
        The function to be plot is:
                    Y = COS(2.pi.X) . e^(-C.X)
        where C is a constant.

        Args:
            delta_factor: It corresponds to the value of the constant C

        Returns:
            Color OpenCV image with the plot of the curve
        '''
        # We create a list of evenly spaced numbers. Since we did not specify
        # the amount of elements in the list, the default value is 50, so if
        # we check the values, we will have 50 numbers in this list, every 0.1.
        # This line will be the X axis values
        x1 = np.linspace(0.0, 5.0, num=200)
        # We make a cosine computation for each X value: The computation is:
        #                  Y = COS(2.pi.X) . e^(- C . X)
        y1 = np.cos(2 * np.pi * x1) * np.exp((-1) * delta_factor * x1)

        # We create a figure to show our graph
        fig = plt.figure()
        # GCA = Get Current Axis, which means the current active figure.
        ax = plt.gca()
        # We make a 2D curve plot, where the X axis is x1, and y1 is the Y axis values
        ax.plot(x1, y1, 'k')
        # We put a title to the plot
        ax.set_title('Cosine function plot, modulated by exponential\nEquation: Y = COS(2.pi.X) . e^(-C.X) with C = {:.2f}'.format(delta_factor))
        # We add a label to the X axis
        ax.set_xlabel('Time (seconds)')
        # We add a label to the Y axis
        ax.set_ylabel('Damped oscillation')
        # We show the grid in the plot
        plt.grid()
        # We draw in the figure all this information. If we make a for loop that
        # updates the data, this function have to be called each time one of the
        # axis values changes. This will give the idea of real time evolution of a curve.
        fig.canvas.draw()
        # We get the RGB buffer that represents our plot., and we code it as in uint8 values
        rgb_img = np.array(fig.canvas.buffer_rgba(), dtype=np.uint8)
        # Since the previous image is RGB, and our OpenCV system expects BGR,
        # we convert the buffer to be in BGR
        img = cv2.cvtColor(rgb_img, cv2.COLOR_RGB2BGR)

        # Do not forget to close the MatPlotLib.pyplot figures, if not, the
        # system memory will overflow quickly
        plt.close('all')

        return img

    def add_image(self):
        '''
        This example shows how we can use the same Image widget we created to
        show images, and show plots created by MatPlotLib library. This is
        important since matplotlib is extremely useful to create bar plots,
        plot functions, in either, 2D or 3D, in an really easy manner.
        Examples of these plots are the histograms, and LUT function plots.
        On the other hand, showing them in Qt is not trivial.
        Nonetheless, since we already have a way to show images, we use it
        to avoid this problem.

        This method converts the matplotlib figure into an image, and after
        being an image, we can show it as any other image matrix.

        In order to show a nice application, we make the plot to evolve.
        By using a timer, we modulate the exponential function constant
        each time the timer times out, and we recompute the curve, and we update
        the ImageWidget shown image.
        '''
        # We create our ImageWidget object
        self.image_widget_top = ImageWidget(self)
        # We create our plot with matplotlib and we convert it into an OpenCV Image
        img = self.create_matplotlib_plot_img(self.factor)
        # We update the shown image with our plot
        self.image_widget_top.updateImage(img)
        # We add the ImageWidget to the left layout
        self.left_layout.addWidget(self.image_widget_top)

        # We create a QTimer that will periodically update the ImageWidget
        self.timer = QTimer(self)
        # We set a periodic mode, by setting the singleShot feature to False
        self.timer.setSingleShot(False)
        # We connect the Timeout signal of the timer with the self.on_timer_timeout
        # slot
        self.timer.timeout.connect(self.on_timer_timeout)
        # We start the timer, with a period of 100mS
        self.timer.start(100)

    def on_timer_timeout(self):
        '''
        Slot called each time the timer times out.
        '''
        # We modify the constant C of the equation. The sign can change, and
        # the amount we modify the constant is always equal to 0.01.
        self.factor += self.constant_sign * 0.01
        # If the absolute value of the constant C is higher than 1, we change
        # the direction of change
        if abs(self.factor) > 1:
            self.constant_sign *= -1
            self.factor += self.constant_sign * 0.01

        # We modify our image to be shown, changing the constant value
        img = self.create_matplotlib_plot_img(self.factor)
        # We update the shown image with our plot
        self.image_widget_top.updateImage(img)