from PySide6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QSlider, QTextEdit, QDockWidget, QLabel, QListWidget, QVBoxLayout, QWidget, QHBoxLayout, QFrame, QListWidgetItem
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QImage
from ui import CircleCanvas

class HistoryWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.title = QLabel("History")
        self.title.setStyleSheet('font-size: 20px; font-weight: bold;')
        layout.addWidget(self.title)
        self.layers_layout = QVBoxLayout()

        self.map = CircleCanvas()
        layout.addWidget(self.map)

        self.list = QListWidget()
        self.list.setDragDropMode(QListWidget.InternalMove)

        for i in range(10):
            layour = QHBoxLayout()
            label1 = QLabel(f"{i}. new thing")
            line = QFrame()
            line.setFrameShape(QFrame.VLine)
            line.setFrameShadow(QFrame.Sunken)
            label = QLabel("layer1")
            layour.addWidget(label1)
            layour.addWidget(line)
            layour.addWidget(label)
            widget = QWidget()
            widget.setLayout(layour)
            item = QListWidgetItem()
            item.setSizeHint(widget.sizeHint())
            self.list.addItem(item)
            self.list.setItemWidget(item, widget)
            #self.layers_layout.addLayout(layour)
        self.layers_layout.addWidget(self.list)
        self.layers_layout.setSpacing(1)
        #layout.setContentsMargins(0, 0, 0, 0)

        self.commit_name = QLabel("History")
        self.commit_name.setStyleSheet('font-size: 20px; font-weight: bold;')
        layout.addWidget(self.commit_name)

        layout.addLayout(self.layers_layout)

        self.setLayout(layout)
