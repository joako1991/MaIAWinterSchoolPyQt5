from PyQt5.QtWidgets import \
    QScrollArea, \
    QHBoxLayout, \
    QMainWindow, \
    QVBoxLayout, \
    QWidget, \
    QPushButton, \
    QSpinBox, \
    QFormLayout, \
    QFileDialog, \
    QLabel, \
    QGroupBox, \
    QRadioButton, \
    QLayout, \
    QDoubleSpinBox

from image_widget import ImageWidget
from fourier_filter import FourierFilter
import cv2
import numpy as np

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
        self.fourier_filter = None
        self.selected_filter = -1

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
        self.add_image_widget()
        self.add_open_image_button()
        self.add_change_width_spinbox()
        self.add_filtering_widget()

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
        self.filtered_fourier_image = ImageWidget(parent=self, enable_click=True)
        self.output_image = ImageWidget(parent=self, enable_click=False)

        self.left_layout.addWidget(self.output_image)
        self.left_layout.addWidget(self.filtered_fourier_image)

    def add_open_image_button(self):
        button = QPushButton('Open new image...', self)

        self.right_layout.addWidget(button)

        button.clicked.connect(self.on_open_image)

    def add_change_width_spinbox(self):
        self.spinbox = QSpinBox(self)
        label = QLabel("Image width:", self)
        form_layout = QFormLayout()
        form_layout.addRow(label, self.spinbox)
        temp_widget = QWidget()
        temp_widget.setLayout(form_layout)

        self.spinbox.setMaximum(10000)
        self.spinbox.setMinimum(2)
        self.spinbox.setSingleStep(10)
        self.spinbox.setValue(480)

        self.right_layout.addWidget(temp_widget)

        self.spinbox.valueChanged.connect(self.on_new_width_set)

    def add_filtering_widget(self):
        self.fourier_filter = FourierFilter()
        self.selected_filter = self.fourier_filter.HIGH_PASS_FILTER
        remove_button = QPushButton('Undo filter', self)
        self.filter_radius = QDoubleSpinBox(self)
        label = QLabel("Filter Radious:", self)
        form_layout = QFormLayout()
        form_layout.addRow(label, self.filter_radius)
        temp_widget = QWidget()
        temp_widget.setLayout(form_layout)

        self.filter_radius.setMaximum(10000)
        self.filter_radius.setMinimum(0.1)
        self.filter_radius.setSingleStep(1)
        self.filter_radius.setValue(3)

        group_box = QGroupBox("Filter selection")

        radio1 = QRadioButton("Low pass filter")
        radio2 = QRadioButton("High pass filter")
        radio2.setChecked(True)

        layout = QVBoxLayout()
        layout.addWidget(radio1)
        layout.addWidget(radio2)
        layout.addStretch(1)
        group_box.setLayout(layout)
        layout.setSizeConstraint(QLayout.SetMinimumSize)

        self.right_layout.addWidget(temp_widget)
        self.right_layout.addWidget(remove_button)
        self.right_layout.addWidget(group_box)

        radio1.toggled.connect(self.on_low_pass_selected)
        radio2.toggled.connect(self.on_high_pass_selected)
        remove_button.clicked.connect(self.on_undo_filter)
        self.filtered_fourier_image.imageClicked.connect(self.on_add_filter)

    def on_low_pass_selected(self, state):
        if state:
            self.selected_filter = self.fourier_filter.LOW_PASS_FILTER

    def on_high_pass_selected(self, state):
        if state:
            self.selected_filter = self.fourier_filter.HIGH_PASS_FILTER

    def update_images(self):
            self.filtered_fourier_image.updateImage(self.fourier_filter.get_image_fft())
            filtered_image = np.absolute(np.fft.ifft2(np.fft.ifftshift(self.fourier_filter.current_fourier_transform)))
            filtered_image = np.array(filtered_image, dtype=np.uint8)
            self.output_image.updateImage(filtered_image)

    def on_undo_filter(self):
        if self.filtered_fourier_image.opencv_image.size:
            self.fourier_filter.remove_last_filter()
            self.update_images()

    def on_add_filter(self, row, column):
        if self.filtered_fourier_image.opencv_image.size:
            radius = self.filter_radius.value()
            self.fourier_filter.add_filter(self.selected_filter, radius, row, column)
            self.update_images()

    def on_new_width_set(self, value):
        self.output_image.changeImageWidth(value)
        self.filtered_fourier_image.changeImageWidth(value)

    def on_open_image(self):
        # We create an explorer dialog object, and we execute it immediately.
        # This dialog will have a title "Open FIle", and it will filter the files
        # to only show the ones that finishes with .png in their filename
        filepath = (QFileDialog.getOpenFileName(self,
            'Open file',
            '',
            "Image files ( *.png *.jpg *.gif *.jpeg )"))[0]
        # If the user has chosen correctly the file, the fname[0] will be an
        # string with the filepath of it
        if filepath:
            img = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE | cv2.IMREAD_ANYDEPTH)
            self.initialize_images(img)
        else:
            print("No path value entered.")

    def initialize_images(self, new_img):
        self.output_image.clearBuffers()
        self.filtered_fourier_image.clearBuffers()
        self.fourier_filter.reset_filtering()

        if not new_img is None:
            self.fourier_filter.update_image(new_img)
            self.update_images()