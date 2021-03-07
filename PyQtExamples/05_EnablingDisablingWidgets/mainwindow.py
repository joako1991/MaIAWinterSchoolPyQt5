from PyQt5.QtWidgets import \
    QHBoxLayout, \
    QMainWindow, \
    QPushButton, \
    QRadioButton, \
    QScrollArea, \
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

        self.is_enabled = True
        self.button = None
        self.radio = None

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
        self.add_buttons()

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

    def add_buttons(self):
        '''
        Add a normal Push Button and a radio button. The Push button will enable
        or disable the Radio button. The radio button has no functionality, just
        to show the effect of disabing a widget.
        '''
        # We create a push button object
        self.button = QPushButton("Disable", self)
        # We connect the signal that tells the push button has been pressed, with
        # the slot self.on_button_pushed
        self.button.clicked.connect(self.on_button_pushed)

        # We create the radio button and we set it as checked
        self.radio = QRadioButton("My radio Button", self)
        self.radio.setChecked(True)

        # We add the two buttons to the right layout
        self.right_layout.addWidget(self.button)
        self.right_layout.addWidget(self.radio)

    def on_button_pushed(self):
        '''
        Slot executed whenever we push the QPushButton. It will change the state
        of the radio button from disable to enable, and vice-versa.
        '''
        # We switch the state of the is_enable variable. ^ is the XOR operator.
        # Since is_enabled is boolean, it can have the value True or False,
        # but inside, it is just 0 (False) or 1 (True). If we do A XOR B, if both A and B are
        # equal, the result is zero. If A and B are different, the result is one.
        # So, if we do is_enabled XOR True, if is_enabled is False, the result is True.
        # If is_enabled is True, the result is False. Therefore, it toggles the
        # state of the variable each time we call this function.
        self.is_enabled ^= True

        # We set the state to enabled if self.is_enabled is True, or disable if
        # it is False.
        self.radio.setEnabled(self.is_enabled)
        # Now, we change the text of the QPushButton to "Disable" or "Enable",
        # depending on the value of self.is_enabled
        if self.is_enabled:
            self.button.setText("Disable")
        else:
            self.button.setText("Enable")