from PySide6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QSlider, QTextEdit, QDockWidget, QLabel, QListWidget, QVBoxLayout, QWidget, QHBoxLayout, QFrame, QListWidgetItem
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QImage

from core import signal_bus
from ui import CircleCanvas

class HistoryWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.bus = signal_bus
        self.bus.update_history.connect(self.add_history)
        layout = QVBoxLayout()
        self.title = QLabel("History")
        self.title.setStyleSheet('font-size: 20px; font-weight: bold;')
        layout.addWidget(self.title)
        self.layers_layout = QVBoxLayout()

        self.map = CircleCanvas()
        layout.addWidget(self.map)

        self.list = QListWidget()
        #self.list.setDragDropMode(QListWidget.InternalMove)

        self.layers_layout.addWidget(self.list)
        self.layers_layout.setSpacing(1)
        #layout.setContentsMargins(0, 0, 0, 0)

        self.commit_name = QLabel("History")
        self.commit_name.setStyleSheet('font-size: 20px; font-weight: bold;')
        layout.addWidget(self.commit_name)

        layout.addLayout(self.layers_layout)

        self.setLayout(layout)

    def add_history(self, history):
        layout = QHBoxLayout()
        layout.addWidget(QLabel(history["layer"]))
        line = QFrame()
        line.setFrameShape(QFrame.VLine)
        line.setFrameShadow(QFrame.Sunken)
        layout.addWidget(line)
        layout.addWidget(QLabel(history["title"]))
        line = QFrame()
        line.setFrameShape(QFrame.VLine)
        line.setFrameShadow(QFrame.Sunken)
        layout.addWidget(line)
        layout.addWidget(QLabel(history["date"]))
        widget = QWidget()
        widget.setLayout(layout)
        item = QListWidgetItem()
        item.setSizeHint(widget.sizeHint())
        self.list.addItem(item)
        self.list.setItemWidget(item, widget)
        #self.layers_layout.addLayout(layour)
