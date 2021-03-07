from PyQt5.QtWidgets import \
    QScrollArea, \
    QHBoxLayout, \
    QMainWindow, \
    QVBoxLayout, \
    QWidget

from image_widget import ImageWidget

import cv2
import os

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

        self.image_widget_top = None
        self.image_widget_bottom = None

        self.initialize_widget()
        self.setWindowTitle("This is my example of how to show an image")

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
        self.add_image_widget()

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

    def add_image_widget(self):
        '''
        This function adds a widget that can show an image. This widget is
        custom, which means, it is implemented by us and not by Qt. If we have
        a matrix either in gray level, or in color, we can use this widget to
        show it.

        This widget shows a fixed width image, which means, the aspect ratio is
        kept, but the width is fixed, it does not matter the image size. So, all the images
        shown using this widget will have the same width.
        '''
        # We create two instances of the custom class, to load two images
        self.image_widget_top = ImageWidget(self)
        self.image_widget_bottom = ImageWidget(self)

        # We load an image to show
        root_dir = os.path.dirname(os.path.realpath(__file__))
        filepath = os.path.join(root_dir, 'images/Lenna_GL.png')
        img = cv2.imread(filepath, cv2.IMREAD_ANYCOLOR | cv2.IMREAD_ANYDEPTH)
        if not img is None:
            self.image_widget_top.updateImage(img)

        # We load another image to show
        filepath = os.path.join(root_dir, 'images/Lenna.png')
        img2 = cv2.imread(filepath, cv2.IMREAD_ANYCOLOR | cv2.IMREAD_ANYDEPTH)
        if not img2 is None:
            self.image_widget_bottom.updateImage(img2)

        # We add the widget to the Left layout
        self.left_layout.addWidget(self.image_widget_top)
        self.left_layout.addWidget(self.image_widget_bottom)