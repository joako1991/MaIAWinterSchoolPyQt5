from PyQt5.QtWidgets import \
    QWidget, \
    QVBoxLayout

from PyQt5.QtCore import \
    pyqtSignal

import numpy as np
import cv2
import copy

class ChangeColorHSV(QWidget):
    resultReady = pyqtSignal(np.ndarray)

    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)
        self.image = None
        self.initialize_widget()

    def initialize_widget(self):
        layout = QVBoxLayout()
        # Put your widgets here
        self.setLayout(layout)

    def update_image(self, img):
        self.image = img

    def clear_image(self):
        self.image = None

    def on_process_image(self, value):
        if not self.image is None:
            output = self.image
            self.resultReady.emit(output)