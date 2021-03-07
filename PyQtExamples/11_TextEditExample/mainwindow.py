from PyQt5.QtWidgets import \
    QHBoxLayout, \
    QMainWindow, \
    QScrollArea, \
    QTextEdit, \
    QVBoxLayout, \
    QWidget

from PyQt5.QtCore import \
    Qt

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

        self.plain_text_box = None

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
        self.add_plain_text_edit()

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

    def add_plain_text_edit(self):
        '''
        This function adds a Text edit box. This object allows to add several
        lines of text, that we can retrieve at the end. In this case, we set
        it as read-only, which means we cannot write by the user interface, but
        we can add text using lines of code. We can modify several of its
        parameters in order to make a better text: Alignment, italic, bold,
        letter size, letter type, etc, as in any text editor like Word from Microsoft or
        Writer from OpenOffice.
        '''
        # We create our QTextEdit object
        self.plain_text_box = QTextEdit(self)
        # We change it to be read-only, because we do not want the user to
        # write text
        self.plain_text_box.setReadOnly(True)

        # We add a line at the bottom of all the text
        self.plain_text_box.append("Hello")

        # We add another line at the bottom of all the text
        self.plain_text_box.append("My")
        # We change the alignment of the last inserted text
        self.plain_text_box.setAlignment(Qt.AlignCenter)

        # We add another line at the bottom of all the text
        self.plain_text_box.append("World")
        # We change the alignment of the last inserted text
        self.plain_text_box.setAlignment(Qt.AlignRight)

        # We add our widget to the left layout
        self.left_layout.addWidget(self.plain_text_box)