from PyQt5.QtWidgets import \
    QLabel, \
    QSlider, \
    QVBoxLayout, \
    QWidget

from PyQt5.QtCore import \
    Qt, \
    pyqtSignal

'''
This class wraps the QSlider from Qt. It adds a label that shows the actual
slider value.

This slider is horizontal and it shows ticks for each possible value. This class
also contains a signal that is emitted whenever the slider value changed.
'''
class SliderWithLabel(QWidget):
    # Signal emitted each time the slider value changes.
    valueChanged = pyqtSignal(int)

    def __init__(self, min_val, max_val, parent=0):
        '''
        Constructor.

        Args:
            min_val: Minimum allowed slider value
            max_val: Maximum allowed slider value
        '''
        super(QWidget, self).__init__(parent)
        self.slide_bar = None
        self.tick_label = None

        ## Slider orientation. We can set it as horizontal or vertical
        self.slider_orientation = Qt.Horizontal
        # self.slider_orientation = Qt.Vertical

        self.initialize_widget(min_val, max_val)

    def initialize_widget(self, min_val, max_val):
        '''
        Initialize the slider widget. It will add the ticks to the qslider,
        and it will add a label that will hold the actual slider value. It sets
        also the maximum and minimum slider values.

        Args:
            min_val: Minimum allowed slider value
            max_val: Maximum allowed slider value
        '''
        ## We create an slider with the ticks marks, in the desired orientation
        self.slide_bar = QSlider(orientation=self.slider_orientation, parent=self)
        self.slide_bar.setTickPosition(QSlider.TicksBelow)

        # We set the maximum and minimum values the slider can take
        self.slide_bar.setMaximum(max_val)
        self.slide_bar.setMinimum(min_val)

        ## Each time the slider value changes, it will call the function
        # self.on_slider_changed
        self.slide_bar.valueChanged.connect(self.on_slider_changed)

        # We change the maximum and minimum value that can be set on the slider
        self.slide_bar.setMinimum(min_val)
        self.slide_bar.setMaximum(max_val)

        # We create a label that contains the actual slider value.
        # We initialize it in zero
        self.tick_label = QLabel('{}'.format(min_val))

        # We place the slider and below it, the label
        layout = QVBoxLayout()
        layout.addWidget(self.slide_bar)
        layout.addWidget(self.tick_label)

        self.setLayout(layout)

    def on_slider_changed(self, value):
        '''
        Function called each time the slider value changed.

        Args:
            value: New slider value
        '''
        # We update the label value
        self.tick_label.setText('{}'.format(value))
        self.valueChanged.emit(value)
