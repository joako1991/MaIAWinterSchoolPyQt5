from PyQt5.QtWidgets import \
    QDoubleSpinBox, \
    QHBoxLayout, \
    QLabel, \
    QMainWindow, \
    QScrollArea, \
    QSpinBox, \
    QVBoxLayout, \
    QWidget

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

        self.spin_box = None
        self.double_spin_box = None

        self.initialize_widget()
        self.setWindowTitle("This is my SpinBox example")

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
        self.add_spin_box()
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

    def add_spin_box(self):
        '''
        This function adds two spin boxes: One with integers numbers, and the
        other one, for decimal numbers.

        We set the maximum and minimum values to be in the range [10, 100] in both cases.
        Whenever the SpinBoxes values changes, a callback function is called
        to print the new value set.

        We also add two labels in the sides, in order to identify what the spinboxes
        changes. In these examples, the names are random, and they have no meaning.
        '''
        ## Integers spinbox.
        # We create the SpinBox object
        self.spin_box = QSpinBox(self)
        # We set its minimum - maximum possible values. If the user tries to put a number
        # out of this range, the spinbox will not allow it.
        self.spin_box.setRange(10, 100)
        # We add a suffix to the value (for instance, the unit of the variable
        # controlled by the spinbox)
        self.spin_box.setSuffix(" pixels")
        # We set an step. This step tells how many units the spinbox will move
        # when we use the arrows aside the spin box. In this case,
        # the spinbox value will change by + / - 2 units when we use those arrows
        self.spin_box.setSingleStep(2)

        # This line connects the signal that informs each time the spinbox value
        # has changed, with the function self.on_spinbox_value_changed.
        self.spin_box.valueChanged.connect(self.on_spinbox_value_changed)

        # We Put a label aside the SpinBox
        # In order to do that, we create a temporal widget, and we set its layout
        # to be the layout that contains both, the label and the spinbox. This
        # temporal widget is the one we add to the right layout.
        label = QLabel("X Offset:", self)
        hor_layout = QHBoxLayout()
        tempWidget = QWidget()
        hor_layout.addWidget(label)
        hor_layout.addWidget(self.spin_box)
        tempWidget.setLayout(hor_layout)

        # We add the label and spinbox widget to the right layout
        self.right_layout.addWidget(tempWidget)

        # Decimal spinbox.
        # We create the SpinBox object
        self.double_spin_box = QDoubleSpinBox(self)
        # We set its minimum - maximum possible values. If the user tries to put a number
        # out of this range, the spinbox will not allow it.
        self.double_spin_box.setRange(10, 100)
        # We add a suffix to the value (for instance, the unit of the variable
        # controlled by the spinbox)
        self.double_spin_box.setSuffix(" pixels")
        # We set an step. This step tells how many units the spinbox will move
        # when we use the arrows aside the double spin box. In this case,
        # the spinbox value will change by + / - 0.01 units when we use those arrows
        self.double_spin_box.setSingleStep(0.01)
        # This line connects the signal that informs each time the double spinbox value
        # has changed, with the function self.on_double_spinbox_value_changed.
        self.double_spin_box.valueChanged.connect(self.on_double_spinbox_value_changed)

        # We Put a label aside the SpinBox
        doubleLabel = QLabel("Y Offset:", self)
        double_hor_layout = QHBoxLayout()
        doubleTempWidget = QWidget()
        double_hor_layout.addWidget(doubleLabel)
        double_hor_layout.addWidget(self.double_spin_box)
        doubleTempWidget.setLayout(double_hor_layout)

        # We add the temporal widget to the right layout
        self.right_layout.addWidget(doubleTempWidget)


    def on_spinbox_value_changed(self, value):
        print("The SpinBox has changed its value to {} pixels".format(value))
        # Here you add your code to use the new spinbox value

    def on_double_spinbox_value_changed(self, value):
        print("The Double SpinBox has changed its value to {} pixels".format(value))
        # Here you add your code to use the new double spinbox value