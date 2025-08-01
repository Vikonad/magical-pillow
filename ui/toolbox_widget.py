from PySide6.QtWidgets import (
    QGridLayout,
    QApplication, QMainWindow, QPushButton, QSlider, QTextEdit, QDockWidget, QLabel, QListWidget, QVBoxLayout, QWidget, QHBoxLayout, QFrame, QListWidgetItem
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QImage
from ui import CircleCanvas

from random import randrange

class ToolboxWidget(QWidget):
    def __init__(self):
        super().__init__()
        #self.setFixedWidth(100)
        layout = QVBoxLayout()

        options = [
            [["drawing"],["text"]],
            [["filters"],["effects"]],
            [["analysis"],["utility"]],
            [["animations"]],
            [["colors manipulation"]],
            [["transformations"]],
        ]
        for i in options:
            buttons_layout = QHBoxLayout()
            for j in i:
                button = QPushButton(j[0])
                print(len(i))
                print(j)
                if len(i) > 1:
                    buttons_layout.addWidget(button)
                    layout.addLayout(buttons_layout)
                else: layout.addWidget(button)



        #drawing = QPushButton("Drawing and Text")
        #layout.addWidget(drawing)
        #filters = QPushButton("Filters and Effects")
        #layout.addWidget(filters)
        #colorman = QPushButton("Color Manipulation")
        #layout.addWidget(colorman)
        #transformations = QPushButton("Transformations and Geometry")
        #layout.addWidget(transformations)
        #animation = QPushButton("GIFs and Animation")
        #layout.addWidget(animation)
        #analysis = QPushButton("Analysis and Utilities")
        #layout.addWidget(analysis)

        layout.addStretch()


        self.setLayout(layout)
