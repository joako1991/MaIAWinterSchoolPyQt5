from PyQt5.QtWidgets import \
    QScrollArea, \
    QHBoxLayout, \
    QMainWindow, \
    QVBoxLayout, \
    QWidget

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
        main_scroll = QScrollArea()

        # The MainWindow is splitted into two areas, left and right, each of them
        # with the corresponding layouts
        left_widget = QWidget()
        right_widget = QWidget()
        main_widget = QWidget()

        left_widget.setLayout(self.left_layout)
        self.right_layout.addStretch(1)
        right_widget.setLayout(self.right_layout)

        self.main_layout.addWidget(left_widget)
        self.main_layout.addStretch(1)
        self.main_layout.addWidget(right_widget)
        main_widget.setLayout(self.main_layout)

        main_scroll.setWidget(main_widget)
        main_scroll.setWidgetResizable(True)

        self.setCentralWidget(main_scroll)

    def create_matplotlib_plot_img(self):
        '''
        This function creates a 2D curve plot to show as an image in our MainWindow.
        The equation of the curve is:
                         Y = COS(2.pi.X) . e^(-X)

        Returns:
            Color OpenCV image with the plot of the curve
        '''
        # We create a list of evenly spaced numbers. Since we did not specify
        # the amount of elements in the list, the default value is 50, so if
        # we check the values, we will have 50 numbers in this list, every 0.1.
        # This line will be the X axis values
        x1 = np.linspace(0.0, 5.0)
        # We make a cosine computation for each X value: The computation is:
        #                  Y = COS(2.pi.X) . e^(-X)
        y1 = np.cos(2 * np.pi * x1) * np.exp(-x1)

        # We create a figure to show our graph
        fig = plt.figure()
        # GCA = Get Current Axis, which means the current active figure.
        ax = plt.gca()
        # We make a 2D curve plot, where the X axis is x1, and y1 is the Y axis values
        ax.plot(x1, y1, 'ko-')
        # We put a title to the plot
        ax.set_title('Cosine function plot, modulated by exponential')
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

    def create_matplotlib_bar_img(self):
        '''
        This function creates a 2D bar plot to show as an image in our MainWindow.
        '''
        # We create a list of evenly spaced numbers. Since we did not specify
        # the amount of elements in the list, the default value is 50, so if
        # we check the values, we will have 50 numbers in this list, every 0.1.
        # This line will be the X axis values
        x1 = np.linspace(0.0, 5.0)
        # We make a cosine computation for each X value: The computation is:
        #                  Y = COS(2.pi.X) . e^(-X)
        y1 = np.cos(2 * np.pi * x1) * np.exp(-x1)

        # We create a figure to show our graph
        fig = plt.figure()
        # GCA = Get Current Axis, which means the current active figure.
        ax = plt.gca()
        # We make a bar plot, where the X axis is x1, and y1 is the Y axis values
        ax.bar(x1, y1)
        # We put a title to the plot
        ax.set_title('Cosine function plot, modulated by exponential')
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
        being an image, we can show it as any other image matrix. In this case,
        we show two graphs, that demostrates that in both cases, the procedure is
        the same: We create our figure, we add all the information we want (
        title, axis labels, grid, legend, axis limits, etc) and then, instead
        of calling matplotlib.pyplot.show, we use the current figure to extract
        the RGB data, and convert it into an image in the BGR space. Once there,
        we just update the shown image in the ImageWidget.
        '''
        # We create our ImageWidget object
        self.image_widget_top = ImageWidget(self)
        # We create our plot with matplotlib and we convert it into an OpenCV Image
        img = self.create_matplotlib_plot_img()
        # We update the shown image with our plot
        self.image_widget_top.updateImage(img)
        # We add the ImageWidget to the left layout
        self.left_layout.addWidget(self.image_widget_top)

        # We create another ImageWidget object
        self.image_widget_bottom = ImageWidget(self)
        # We create our plot with matplotlib and we convert it into an OpenCV Image
        img = self.create_matplotlib_bar_img()
        # We update the shown image with our plot
        self.image_widget_bottom.updateImage(img)
        # We add the ImageWidget to the left layout
        self.left_layout.addWidget(self.image_widget_bottom)