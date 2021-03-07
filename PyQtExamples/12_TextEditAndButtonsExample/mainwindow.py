from PyQt5.QtWidgets import \
    QHBoxLayout, \
    QLineEdit, \
    QMainWindow, \
    QPushButton, \
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
        self.line_edit = None
        self.text_alignment = 0

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
        This function adds a line edit box, two buttons and a text edit box.
        With it, we can insert a line of text, and when we push the insert button,
        it appends this text to the text edit box. The second button is to
        clear the text box.

        Additionally, each inserted line is placed at the opposite alignment
        of the previous line.
        '''
        # We create our QTextEdit object
        self.plain_text_box = QTextEdit(self)
        # We change it to be read-only, because we do not want the user to
        # write text
        self.plain_text_box.setReadOnly(True)
        # We set the text style as Italic
        self.plain_text_box.setFontItalic(True)
        # We change the font family to Arial
        self.plain_text_box.setFontFamily('Arial')
        # We change the letter size to 15
        self.plain_text_box.setFontPointSize(15)

        # We add a button to insert the text in the line edit into the text edit box.
        insert_button = QPushButton("Add text", self)
        # We connect the insert button clicked signal with the slot self.on_insert_push_button
        insert_button.clicked.connect(self.on_insert_push_button)

        # We add a button to clear the text edit box.
        clear_button = QPushButton("Clear all", self)
        # We connect the clear button clicked signal with the slot self.on_clear_push_button
        clear_button.clicked.connect(self.on_clear_push_button)

        # We add a line edit object
        self.line_edit = QLineEdit(self)
        # We set the line edit help text (place holder text)
        self.line_edit.setPlaceholderText("Insert your text here...")

        # We add our widgets to the left layout in order: Edit line, insert
        # button, text box, clear button
        self.left_layout.addWidget(self.line_edit)
        self.left_layout.addWidget(insert_button)
        self.left_layout.addWidget(self.plain_text_box)
        self.left_layout.addWidget(clear_button)

    def on_insert_push_button(self):
        '''
        This function is called each time the insert button is pressed.
        Each time this function is called, the inserted text is aligned
        either to the left, or to the right. Each time, it swtiches automatically
        the alignment.
        '''
        if self.line_edit.text():
            # We switch the alignment variable. If it is 0, we align the text to the left,
            # If it is 1, we align it to the right
            self.text_alignment ^= 1
            # We read the edit line, and we add this line to the text box.
            self.plain_text_box.append(self.line_edit.text())
            # We change the alignment of the last inserted line
            if self.text_alignment:
                # If self.text_alignment is 1, we align to the right
                self.plain_text_box.setAlignment(Qt.AlignRight)
            else:
                # If self.text_alignment is 0, we align to the left
                self.plain_text_box.setAlignment(Qt.AlignLeft)
            # We clear the line edit once we finished
            self.line_edit.clear()
        else:
            print("No phrase inserted!")

    def on_clear_push_button(self):
        '''
        Slot executed each time we push the text edit clear button. It will
        erase all the content of the text edit box.
        '''
        self.plain_text_box.clear()