from PySide6.QtWidgets import (
    QGridLayout,
    QApplication, QMainWindow, QPushButton, QSlider, QTextEdit, QDockWidget, QLabel, QListWidget, QVBoxLayout, QWidget, QHBoxLayout, QFrame, QListWidgetItem
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QImage
from core import SignalBus

from random import randrange

class ToolboxWidget(QWidget):
    def __init__(self):
        super().__init__()
        #self.setFixedWidth(100)
        self.bus = SignalBus()
        self.bus.update_ui_configuration.connect(self.update_ui_configuration)
        layout = QVBoxLayout()

        layout1 = QHBoxLayout()
        layout2 = QHBoxLayout()
        layout3 = QHBoxLayout()

        self.drawing = QPushButton("drawing")
        self.drawing.setCheckable(True)
        self.drawing.toggled.connect(lambda checked: self.bus.toolbox_update.emit([checked, ["drawing","bottom_left_layout"]]))
        layout1.addWidget(self.drawing)

        self.text = QPushButton("text")
        self.text.setCheckable(True)
        self.text.toggled.connect(lambda checked: self.bus.toolbox_update.emit([checked, ["text","bottom_middle_widget"]]))
        layout1.addWidget(self.text)

        layout.addLayout(layout1)

        self.filters = QPushButton("filters")
        self.filters.setCheckable(True)
        self.filters.toggled.connect(lambda checked: self.bus.toolbox_update.emit([checked, ["filters","bottom_left_layout"]]))
        layout2.addWidget(self.filters)

        self.effects = QPushButton("effects")
        self.effects.setCheckable(True)
        self.effects.toggled.connect(lambda checked: self.bus.toolbox_update.emit([checked, ["effects","bottom_left_layout"]]))
        layout2.addWidget(self.effects)

        layout.addLayout(layout2)

        self.analysis = QPushButton("analysis")
        self.analysis.setCheckable(True)
        #self.analysis.toggled.connect(lambda checked: self.bus.toolbox_update.emit([checked, ["analysis","bottom_left_layout"]]))
        layout3.addWidget(self.analysis)

        self.utility = QPushButton("utility")
        self.utility.setCheckable(True)
        #self.utility.toggled.connect(lambda checked: self.bus.toolbox_update.emit([checked, ["effects","bottom_left_layout"]]))
        layout3.addWidget(self.utility)

        layout.addLayout(layout3)

        self.animations = QPushButton("animations")
        self.animations.setCheckable(True)
        #self.text.toggled.connect(lambda checked: self.bus.toolbox_update.emit([checked, ["effects","bottom_left_layout"]]))
        layout.addWidget(self.animations)

        self.colors = QPushButton("colors manipulation")
        self.colors.setCheckable(True)
        #self.text.toggled.connect(lambda checked: self.bus.toolbox_update.emit([checked, ["effects","bottom_left_layout"]]))
        layout.addWidget(self.colors)

        self.transformations = QPushButton("transformations")
        self.transformations.setCheckable(True)
        #self.text.toggled.connect(lambda checked: self.bus.toolbox_update.emit([checked, ["effects","bottom_left_layout"]]))
        layout.addWidget(self.transformations)

        self.setLayout(layout)

    def update_ui_configuration(self, configuration):
        self.bus.toolbox_update.emit([configuration["drawing"],["drawing","bottom_left_layout"]])
        self.drawing.setChecked(configuration["drawing"])
        self.bus.toolbox_update.emit([configuration["text"],["text","bottom_middle_widget"]])
        self.text.setChecked(configuration["text"])
        self.bus.toolbox_update.emit([configuration["filters"],["filters","bottom_left_layout"]])
        self.filters.setChecked(configuration["filters"])
        self.bus.toolbox_update.emit([configuration["effects"],["effects","bottom_left_layout"]])
        self.effects.setChecked(configuration["effects"])
