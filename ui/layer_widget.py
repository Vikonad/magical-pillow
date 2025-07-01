from PySide6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QSlider, QTextEdit, QDockWidget, QLabel, QListWidget, QVBoxLayout, QWidget, QHBoxLayout
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QImage

class LayerWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.layers_layout = QVBoxLayout()
        self.layers_layout.setSpacing(0)
        #layout.setContentsMargins(0, 0, 0, 0)

        layout.addStretch()

        bottom_buttons = QVBoxLayout()
        buttons1 = QHBoxLayout()
        up_button = QPushButton()
        buttons1.addWidget(up_button)

        down_button = QPushButton()
        buttons1.addWidget(down_button)

        delete_layer = QPushButton()
        buttons1.addWidget(delete_layer)

        bottom_buttons.addLayout(buttons1)

        self.add_new_layer = QPushButton("Add new layer")
        bottom_buttons.addWidget(self.add_new_layer)

        layout.addLayout(self.layers_layout)
        layout.addLayout(bottom_buttons)

        self.setLayout(layout)
