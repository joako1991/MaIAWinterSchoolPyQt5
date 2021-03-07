from PyQt5.QtWidgets import \
    QFileDialog, \
    QHBoxLayout, \
    QMainWindow, \
    QPushButton, \
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
        This function creates two buttons, one that is able to open a directory,
        and the other one that can open a file. When we say open, we mean that
        the user can select a given directory, or file, and then we can retrieve
        in code the path of the selection element. This way, we do not need to
        hardcode paths of files in the code, and we can change the files we
        open in a flexible way.
        '''
        # We create a button object to open directories
        button_directory = QPushButton("Open a directory", self)
        # We add the created button to the right layout
        self.right_layout.addWidget(button_directory)
        # We connect the clicked signal to the slot self.on_open_directory
        button_directory.clicked.connect(self.on_open_directory)

        # We create a button object to open files
        button_file = QPushButton("Open a file", self)
        # We add the created button to the right layout
        self.right_layout.addWidget(button_file)
        # We connect the clicked signal to the slot self.on_open_file
        button_file.clicked.connect(self.on_open_file)

    def on_open_directory(self):
        '''
        This slot will show an explorer dialog that will help us to select a
        directory from the system. It is configured to not show files, only
        directories, and when the user clicks on the button "Choose" of this
        dialog, the current path can be retrieved.
        '''
        # We create an explorer dialog object. It does not execute it yet
        dialog = QFileDialog();
        # We set the dialog mode to only be able to choose directories, and not files
        dialog.setFileMode(QFileDialog.DirectoryOnly)
        # We also configure the dialog to only show directories, and hide the files.
        dialog.setOption(QFileDialog.ShowDirsOnly, True)
        # We execute the explorer dialog. If the returned value is true, we can
        # retrieve the selected path as an absolute path
        if(dialog.exec()):
            # We retrieve the absolute path selected
            folder_name = dialog.directory().absolutePath()
            print("You have selected the following directory: {}".format(folder_name))
            # Here you put your code to execute when the directory path is selected
        else:
            print("No path value entered.")

    def on_open_file(self):
        '''
        This slot will show an explorer dialog that will help us to select a
        file from the system. When the user clicks on the button "Choose" of this
        dialog, the selected filepath can be retrieved. If the user did not choose a file,
        the choose button is not enabled.

        We also filter the files to only show the PNG files, which corresponds
        to files that complies with the pattern '*.png'
        '''
        # We create an explorer dialog object, and we execute it immediately.
        # This dialog will have a title "Open FIle", and it will filter the files
        # to only show the ones that finishes with .png in their filename
        fname = QFileDialog.getOpenFileName(self,
            'Open file',
            '',
            "PNG files ( *.png )")
        # If the user has chosen correctly the file, the fname[0] will be an
        # string with the filepath of it
        if fname[0]:
            print("You have selected the file: {}".format(fname[0]))
            # Here you put your code to execute when the filepath is selected
        else:
            print("No path value entered.")