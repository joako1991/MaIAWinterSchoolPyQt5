from PyQt5.QtWidgets import \
    QScrollArea, \
    QHBoxLayout, \
    QMainWindow, \
    QPushButton, \
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
        self.add_button()

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
        '''
        We add a button to the main window.
        '''
        ## We add a button with the legend 'This is my button' on it.
        myButton = QPushButton("This is my button", self)
        # We make a connection between the signal executed whenever the button is pushed
        # and the function self.on_button_clicked. This way, each time we
        # push the button, on_button_clicked is called
        myButton.clicked.connect(self.on_button_clicked)
        ## Once we have our widget, we add it to the layout, so it will be placed
        # in the right place. Without this line, all the widgets will be placed one
        # on top of the other one, in the top left corner of the window
        self.right_layout.addWidget(myButton)

    def on_button_clicked(self):
        # Here you place your actions to execute when you push the button
        print("Hey! You pushed me!!.... THANK YOUUU!!")