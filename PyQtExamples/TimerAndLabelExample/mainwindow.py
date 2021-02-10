from PyQt5.QtWidgets import \
    QScrollArea, \
    QHBoxLayout, \
    QLabel, \
    QMainWindow, \
    QVBoxLayout, \
    QWidget

from PyQt5.QtCore import \
    QTimer

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

        self.counter = 0
        self.label = None
        self.myTimer = None

        self.initialize_widget()
        self.setWindowTitle("This is my timer and label example")

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
        self.add_label_and_timer()

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

    def add_label_and_timer(self):
        '''
        Add a label to the MainWindow. This label will show the value of a counter
        variable. The label text will change every 500 mS, by using a timer. The
        timeout function is self.on_timer_timeout, and it is connected to the
        myTimer.timeout signal.
        '''
        # we create a label that we will change its value every certain amount
        # of time, using the timer.
        self.label = QLabel('{}'.format(self.counter))
        f = QFont("Arial", 20, QFont.Bold);
        self.label.setFont(f);

        self.right_layout.addWidget(self.label)

        # We create our timer.
        self.myTimer = QTimer(self)
        # Everytime the timer timeout value is reach (in this case, 500 mS, set below),
        # the function self.on_timer_timeout will be called
        self.myTimer.timeout.connect(self.on_timer_timeout)

        # If the timer is Single Shot, that means the function on_timer_timeout
        # will be called once. If Single shot is false, then the timer is called
        # all the time, every ccertain time, passed as argument to the myTimer.start
        # function
        self.myTimer.setSingleShot(False)

        # We start a periodic timer, that will execute the function
        # self.on_timer_timeout, every 500 mS
        self.myTimer.start(500)

    def on_timer_timeout(self):
        # We increase the counter value by one. We assign the modulus of counter when its
        # value is divided by 10.
        self.counter = (self.counter + 1) % 20
        # We change the label text with the new counter value
        self.label.setText("{}".format(self.counter))

        # Write here your functions of what you want to do every time the timer
        # timeout is reached

