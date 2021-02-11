from PyQt5.QtWidgets import \
    QHBoxLayout, \
    QLabel, \
    QMainWindow, \
    QPushButton, \
    QScrollArea, \
    QTabWidget, \
    QVBoxLayout, \
    QWidget

from PyQt5.QtGui import \
    QFont

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

        self.button_left = None
        self.button_right = None
        self.tab_widget = None

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
        self.add_tabs()

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

    def create_tab_widget(self, button_name, label_text, callback):
        '''
        This function creates a series of widgets, it adds them in a layout,
        and then it set a widget with that layout. In this case, we add
        only two widgets: A push button, and a label.

        Args:
            button_name: A text with the name that will be shown in the button.
            label_text: A text with what we want to show in the label.
            callback: Function that we want to call each time the button is pushed

        Returns:
            QWidget with a layout that contains the QPushButton and the QLabel
            created.
        '''
        # We create the QPushButton object, with the provided name
        button = QPushButton(button_name, self)
        # We create a label, with the given text
        label = QLabel(label_text)
        # We set the callback for the QPushButton when it is clicked
        button.clicked.connect(callback)

        # We change the label Font, to make it nicer.
        f = QFont("Arial", 20, QFont.Bold)
        label.setFont(f)

        # We create a layout to add the widgets created
        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(button)
        # We create a temporal widget, to which we will set out layout.
        widget = QWidget()
        widget.setLayout(layout)

        # We return the created widget
        return widget

    def add_tabs(self):
        '''
        We create two tabs in the MainWindow. Each tab consists of a single widget.
        But since a widget can be a set of widgets, so we can add several of them
        into each tab. Nonetheless, a layout must be created before, and the
        widget we add should have the layout previously created with all the other
        widgets.

        In this example, we create two tabs, with two widgets each: A push button,
        and a label. The functionality of the push button is to change the tab, directly.
        '''
        # We create the object that will handle the tabs
        self.tab_widget = QTabWidget(self)

        # We add the first tab. Since there are not any other tab, this will have the index 0.
        self.tab_widget.addTab(
            self.create_tab_widget(
                "Change to tab 2",
                "Hello there! I am the Tab 1.\nDo you want to press the button below?\nSomething magic will happen",
                self.on_left_button_pushed),
            "Tab 1")

        # We create another tab. This one, will have the index 1, since the 0 is already occupied.
        self.tab_widget.addTab(
            self.create_tab_widget(
                "Change to tab 1",
                "Oh No!! You have changed the tab!\nNo problem, you can fix it.\nYou just have to press the button below :-D",
                self.on_right_button_pushed),
            "Tab 2")

        # We add the tab to the layout.
        self.right_layout.addWidget(self.tab_widget)

    def on_left_button_pushed(self):
        '''
        Function called each time the first push button is pressed. The action done
        here is just to change the tab. Since this button is placed in the tab
        with index 0, to switch to the second tab we have to specify the index 1.
        '''
        self.tab_widget.setCurrentIndex(1)

    def on_right_button_pushed(self):
        '''
        Function called each time the second push button is pressed. The action done
        here is just to change the tab. Since this button is placed in the tab
        with index 1, to switch to the first tab we have to specify the index 0.
        '''
        self.tab_widget.setCurrentIndex(0)