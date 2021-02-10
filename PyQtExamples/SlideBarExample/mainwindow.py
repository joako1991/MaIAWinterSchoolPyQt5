from PyQt5.QtWidgets import \
    QScrollArea, \
    QFormLayout, \
    QHBoxLayout, \
    QLabel, \
    QMainWindow, \
    QSlider, \
    QVBoxLayout, \
    QWidget

from PyQt5.QtCore import \
    Qt

from slider_with_label import SliderWithLabel


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

        self.slide_bar = None

        self.initialize_widget()
        self.setWindowTitle("This is my buttons example")

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
        self.add_slide_bar()

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
        self.main_layout.addWidget(right_widget)
        main_widget.setLayout(self.main_layout)

        main_scroll.setWidget(main_widget)
        main_scroll.setWidgetResizable(True)

        self.setCentralWidget(main_scroll)

    def add_slide_bar(self):
        '''
        This function adds a new slider in the right side of the MainWindow.
        It is not a base class from Qt. We created a class that wraps the
        basic QSlider, so we add a label with the actual ticks value.
        '''
        self.slide_bar = SliderWithLabel(0, 200, parent=self)

        ## We add a label aside the slider, to identify it. This label says 'This is my Slider'
        label = QLabel("This is my Slider", self)
        slider_widget = QWidget()
        myFormLayout = QFormLayout()
        myFormLayout.addRow(label, self.slide_bar)
        slider_widget.setLayout(myFormLayout)

        ## Each time the slider value changes, it will call the function
        # self.on_slider_changed
        self.slide_bar.valueChanged.connect(self.on_slider_changed)

        # We add the slider to the right layout
        self.right_layout.addWidget(slider_widget)

    def on_slider_changed(self, value):
        ## Here you do what you want with the new slider value
        print("This is my new value {}".format(value))