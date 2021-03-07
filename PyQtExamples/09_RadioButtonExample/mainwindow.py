from PyQt5.QtWidgets import \
    QGroupBox, \
    QLayout, \
    QHBoxLayout, \
    QMainWindow, \
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
        self.add_radio_buttons()

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

    def add_radio_buttons(self):
        '''
        This function shows how to add and use Radio Buttons.

        We also added a groupbox in order to group them all as a block. it
        helps when we want to disable all the buttons at once: We just disable
        the group box. This step of grouping can be avoided. The good thing about
        grouping them is that only one can be activated at once. So when we
        activate another radio button, the previous one gets deactivated
        automatically. If we do not group them, all of them can be activated
        at the same time.

        Each buttons has its own callback, so we can choose what to do in
        each case. Some implementations can be more complex, in a sense that
        all the radio buttons go to the same callback, and inside that callback
        we find which radio button has been checked.
        '''

        # We create the group object that will enclose all the radio buttons.
        # The title of the group is "My group of radio buttons"
        self.group_box = QGroupBox("My group of radio buttons")
        # We create a radio button
        radio1 = QRadioButton("Radio button 1")

        # We set the initial state as the first radio button activated.
        radio1.setChecked(True)

        # We set the callback that will be called EACH TIME THE STATE OF THE
        # RADIO BUTTON CHANGES (it is called in two cases: when the button gets
        # activated, and when it gets deactivated).
        radio1.toggled.connect(self.on_radio_1_toggled)

        # Another radio buttons and its callback
        radio2 = QRadioButton("Radio button 2")
        radio2.toggled.connect(self.on_radio_2_toggled)

        # Another radio buttons and its callback
        radio3 = QRadioButton("Radio button 3")
        radio3.toggled.connect(self.on_radio_3_toggled)


        # We create a layout with all the radio buttons together
        layout = QVBoxLayout()
        layout.addWidget(radio1)
        layout.addWidget(radio2)
        layout.addWidget(radio3)
        # This line helps to compress all the radio buttons to the top of the
        # layout
        layout.addStretch(1)
        # We set this layout to be the layout of the groupbox
        self.group_box.setLayout(layout)

        layout.setSizeConstraint(QLayout.SetMinimumSize)

        # We place this groupbox in the right layout
        self.right_layout.addWidget(self.group_box)

    def on_radio_1_toggled(self, checked):
        '''
        Callback that will be executed each time the state of the radio button 1 changes

        Args:
            checked: If true, it means the radio button has been activated. If
                False, it has been deactivated
        '''
        if checked:
            print("You have activated Radio Button 1")
        else:
            print("Radio button 1 has been deactivated")

    def on_radio_2_toggled(self, checked):
        '''
        Callback that will be executed each time the state of the radio button 2 changes

        Args:
            checked: If true, it means the radio button has been activated. If
                False, it has been deactivated
        '''
        if checked:
            print("You have activated Radio Button 2")
        else:
            print("Radio button 2 has been deactivated")

    def on_radio_3_toggled(self, checked):
        '''
        Callback that will be executed each time the state of the radio button 3 changes

        Args:
            checked: If true, it means the radio button has been activated. If
                False, it has been deactivated
        '''
        if checked:
            print("You have activated Radio Button 3")
        else:
            print("Radio button 3 has been deactivated")