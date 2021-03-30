from PyQt5.QtWidgets import \
    QCheckBox, \
    QDoubleSpinBox, \
    QHBoxLayout, \
    QLabel, \
    QWidget

from PyQt5.QtCore import \
    pyqtSignal, \
    Qt

import numpy as np
import cv2
import copy

class MinMaxWidget(QWidget):
    valueChanged = pyqtSignal(float, float)

    def __init__(self, title, min_val, max_val, parent=None):
        super(QWidget, self).__init__(parent)
        self.image = None
        self.parameter_name = title
        self.min_val = min_val
        self.max_val = max_val
        self.initialize_widget()

    def initialize_widget(self):
        layout = QHBoxLayout()
        label = QLabel(self.parameter_name, self)
        self.enable_check_box = QCheckBox()

        self.min_spin_box = QDoubleSpinBox(self)
        self.min_spin_box.setMinimum(self.min_val)
        self.min_spin_box.setMaximum(self.max_val)

        self.max_spin_box = QDoubleSpinBox(self)
        self.max_spin_box.setMinimum(self.min_val)
        self.max_spin_box.setMaximum(self.max_val)

        layout.addWidget(self.enable_check_box)
        layout.addWidget(label)
        layout.addWidget(self.min_spin_box)
        layout.addWidget(self.max_spin_box)

        # Put your widgets here
        self.setLayout(layout)

        self.enable_check_box.setCheckState(Qt.Checked)
        self.change_widget_enabled(True)

        self.enable_check_box.stateChanged.connect(self.on_state_changed)
        self.min_spin_box.valueChanged.connect(self.on_value_changed)
        self.max_spin_box.valueChanged.connect(self.on_value_changed)

    def is_parameter_enabled(self):
        return bool(self.enable_check_box.checkState() == Qt.Checked)

    def change_widget_enabled(self, enabled):
        self.min_spin_box.setEnabled(enabled)
        self.max_spin_box.setEnabled(enabled)

    def on_state_changed(self, state):
        if state:
            self.change_widget_enabled(True)
        else:
            self.change_widget_enabled(False)

    def on_value_changed(self, value):
        self.blockSignals(True)
        min_val = self.min_spin_box.value()
        max_val = self.max_spin_box.value()
        if min_val > max_val:
            self.min_spin_box.setValue(value)
            self.max_spin_box.setValue(value)

        self.blockSignals(False)
        self.valueChanged.emit(self.min_spin_box.value(), self.max_spin_box.value())

