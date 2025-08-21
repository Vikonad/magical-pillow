from PySide6.QtWidgets import (
    QGridLayout,
    QApplication, QMainWindow, QPushButton, QSlider, QTextEdit, QDockWidget, QLabel, QListWidget, QVBoxLayout, QWidget, QHBoxLayout, QFrame, QListWidgetItem
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QImage
from core import SignalBus
from ui import CircleCanvas

from random import randrange

class ToolboxWidget(QWidget):
    def __init__(self):
        super().__init__()
        #self.setFixedWidth(100)
        self.bus = SignalBus()
        self.bus.update_ui_configuration.connect(self.update_ui_configuration)
        layout = QVBoxLayout()

        self.options = [
            [["drawing", "bottom_left_layout"],["text", "bottom_middle_widget"]],
            [["filters", "bottom_left_layout"],["effects", "bottom_left_layout"]],
            [["analysis"],["utility"]],
            [["animations"]],
            [["colors manipulation"]],
            [["transformations"]],
        ]
        for i in self.options:
            buttons_layout = QHBoxLayout()
            for j in i:
                button = QPushButton(j[0])
                button.setCheckable(True)
                button.toggled.connect(lambda checked, n=j: self.bus.toolbox_update.emit([checked, n]))
                #print(j)
                #button.clicked.connect(lambda checked=False, i=j[1]:self.signal.emit(i))
                if len(i) > 1:
                    buttons_layout.addWidget(button)
                    layout.addLayout(buttons_layout)
                else: layout.addWidget(button)

        self.setLayout(layout)

    def update_ui_configuration(self, configuration):
        self.bus.toolbox_update.emit([configuration["drawing"],self.options[0][0]])
        self.bus.toolbox_update.emit([configuration["text"],self.options[0][1]])
        self.bus.toolbox_update.emit([configuration["filters"],self.options[1][0]])
        self.bus.toolbox_update.emit([configuration["effects"],self.options[1][1]])
