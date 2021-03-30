from PyQt5.QtWidgets import \
    QScrollArea, \
    QHBoxLayout, \
    QMainWindow, \
    QVBoxLayout, \
    QWidget, \
    QPushButton, \
    QFileDialog

from min_max_widget import MinMaxWidget
from image_widget import ImageWidget

import cv2
import numpy as np
import matplotlib.pyplot as plt

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
        self.add_button()
        self.add_images()


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

    def add_button(self):
        button = QPushButton("Ouvrir image", self)
        self.right_layout.addWidget(button)
        button.clicked.connect(self.on_open_image)

    def add_images(self):
        self.img_orig = ImageWidget(self)
        self.hist_orig = ImageWidget(self)
        self.img_sortie = ImageWidget(self)
        self.hist_sortie = ImageWidget(self)

        self.left_layout.addWidget(self.img_orig)
        self.left_layout.addWidget(self.hist_orig)
        self.left_layout.addWidget(self.img_sortie)
        self.left_layout.addWidget(self.hist_sortie)

    def on_open_image(self):
        fname = (QFileDialog.getOpenFileName(self,
            'Open file',
            '',
            "PNG files ( *.png *.jpg *.gif *.jpeg )"))[0]

        if fname:
            img = cv2.imread(fname, cv2.IMREAD_ANYCOLOR | cv2.IMREAD_ANYDEPTH)
            if not img is None:
                self.initialize_images(img)
            # Here you put your code to execute when the filepath is selected
        else:
            print("No path value entered.")

    def create_matplotlib_plot_img(self, img, title):
        amount_bits = img[0,0,0].nbytes * 8
        amount_bins = np.power(2, amount_bits)
        red_hist = (np.histogram(img[:,:,2], bins=range(amount_bins+1)))[0]
        green_hist = (np.histogram(img[:,:,1], bins=range(amount_bins+1)))[0]
        blue_hist = (np.histogram(img[:,:,0], bins=range(amount_bins+1)))[0]

        fig = plt.figure()
        ax = plt.gca()
        ax.plot(red_hist, 'r-')
        ax.plot(green_hist, 'g-')
        ax.plot(blue_hist, 'b-')
        ax.set_title(title)
        ax.set_xlabel('Gray-level')
        ax.set_ylabel('# pixels')
        plt.grid()

        fig.canvas.draw()
        rgb_img = np.array(fig.canvas.buffer_rgba(), dtype=np.uint8)
        img = cv2.cvtColor(rgb_img, cv2.COLOR_RGB2BGR)

        plt.close('all')
        return img

    def initialize_images(self, img):
        self.img_orig.clearBuffers()
        self.hist_orig.clearBuffers()
        self.img_sortie.clearBuffers()
        self.hist_sortie.clearBuffers()

        if not img is None:
            self.img_orig.updateImage(img)
            hist = self.create_matplotlib_plot_img(img, "Histogramme de l'image d'origine")
            self.hist_orig.updateImage(hist)