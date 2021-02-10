from PyQt5.QtWidgets import \
    QScrollArea, \
    QHBoxLayout, \
    QMainWindow, \
    QMessageBox, \
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
        self.main_layout.addStretch(1)
        self.main_layout.addWidget(right_widget)
        main_widget.setLayout(self.main_layout)

        main_scroll.setWidget(main_widget)
        main_scroll.setWidgetResizable(True)

        self.setCentralWidget(main_scroll)

    def add_button(self):
        '''
        This function adds a button to the main window, with which we can 
        execute the QMessageBox we want. 
        '''
        # We create the button object
        button = QPushButton("PUSH ME!!", self)
        # We link the clicked signal with the self.on_button_pushed method
        button.clicked.connect(self.on_button_pushed)
        # We add the button to the layout
        self.right_layout.addWidget(button)

    def on_button_pushed(self):
        '''
        Slot called each time the QPushButton in the main window is pushed.

        It shows a QMessage box. We have set the Icon to Warning, we have editted
        the title, the text, and the informative text fields, and we added
        two buttons: Ok and Cancel. Other buttons are available, just check the
        documentation of QMessageBox: https://doc.qt.io/qt-5/qmessagebox.html
        '''
        # We create the Message box, but it is not executed yet
        msgBox = QMessageBox(self)
        # We modify the window title
        msgBox.setWindowTitle("My first QMessageBox")
        # we change the first line of text
        msgBox.setText("You have pushed the button and then this message box appeared. Isn't great?!?!?")
        # We change the second line text
        msgBox.setInformativeText("Now you can push the button Ok or cancel, and see what it is printed in the terminal")
        # We change the Message Icon (it can be Question, Information, Warning or critical)
        msgBox.setIcon(QMessageBox.Warning)

        # We add two default buttons
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        # We set the default button: This means, if we press enter, it will
        # do the same as clicking the specified button
        msgBox.setDefaultButton(QMessageBox.Ok)

        # We execute the message. This function is blocking, so it will stay here
        # until the user closes in any way, the QMessageBox. When it is closed,
        # one of the added buttons identifier will be returned, so we can act
        # in consequence.
        ret = msgBox.exec()
        # We check what the user entered, and we execute the required actions
        if ret == QMessageBox.Ok:
            # here is your code when the user clicks the Ok button
            print("You pushed the Ok button")
        elif ret == QMessageBox.Cancel:
            # here is your code when the user clicks the Cancel button
            print("You pushed the Cancel button")
        else:
            # This case should never happen: It means that the user entered an
            # option that is not between the available buttons (impossible to happen).
            print("ERROR!!! This should not happen never, if we ask for all the possible buttons before")
