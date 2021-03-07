from PyQt5.QtWidgets import \
    QHBoxLayout, \
    QLabel, \
    QLineEdit, \
    QMainWindow, \
    QPushButton, \
    QScrollArea, \
    QVBoxLayout, \
    QWidget

from PyQt5.QtGui import \
    QFontMetrics

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

        self.line_edit = None
        self.label = None

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
        self.add_button_and_line()

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

    def add_button_and_line(self):
        '''
        This function adds three elements: One line edit to enter text, one
        label to show the last text written, and a push button to confirm
        the entered text.
        '''
        # We create the object with which we will be able to enter a text.
        self.line_edit = QLineEdit(self)
        # We add this object to the right layout
        self.right_layout.addWidget(self.line_edit)

        # We create a label to show the entered text
        self.label = QLabel("No answer entered", self)
        # We add this object to the right layout
        self.right_layout.addWidget(self.label)

        # We create a button to submit the entered text
        button = QPushButton("Submit answer")
        # We add this object to the right layout
        self.right_layout.addWidget(button)

        # We add a placeHolder. This text will be shown in a thin gray color
        # when no text is entered in the line edit object. If any letter or string
        # is written in the line edit, this text will disappear.
        placeHolderText = "Write here your answer..."
        # The pointSize is the amount of pixels a letter takes in the Line edit object.
        # With this line, we compute how many pixels we need, as minimum, for
        # the line edit object, to avoid hiding the Place holder text.
        minimumWidth = self.line_edit.font().pointSize()* len(placeHolderText)
        self.line_edit.setMinimumWidth(minimumWidth)
        # We set the place holder text.
        self.line_edit.setPlaceholderText(placeHolderText)
        # Other options in the line edit object can be set, in order to avoid
        # incorrect characters to be entered, and avoid crashing the program later on.

        # We connect the push button signal clicked with the slot self.on_button_pushed
        button.clicked.connect(self.on_button_pushed)

    def on_button_pushed(self):
        '''
        Slot executed whenever we push the button. In this function, we read
        the text entered in the line edit object, and if the edit line
        is not empty, we set this text in the label object. If it is empty,
        we print a message in the label regarding that.
        '''
        # We read the line edit object
        entered_answer = self.line_edit.text()
        # We check if the entered_answer is empty or not
        if entered_answer:
            # If it is not empty, we set the label with this text
            self.label.setText("Your last answer is: " + entered_answer)
            # We erase everything in the line edit
            self.line_edit.clear()
            # Here is where you place your code when the user entered something
            # in the line edit
        else:
            # Here you place your code when the user does not enter anything.
            self.label.setText("No answer entered")