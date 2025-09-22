from PySide6.QtWidgets import (
    QGridLayout,
    QApplication, QMainWindow, QPushButton, QSlider, QTextEdit, QDockWidget, QLabel, QListWidget, QVBoxLayout, QWidget, QHBoxLayout, QFrame, QListWidgetItem
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QImage
from core import signal_bus

from random import randrange

class ToolboxWidget(QWidget):
    def __init__(self):
        super().__init__()
        #self.setFixedWidth(100)
        self.bus = signal_bus
        self.bus.update_ui_configuration.connect(self.update_ui_configuration)
        layout = QVBoxLayout()

        layout1 = QHBoxLayout()
        layout2 = QHBoxLayout()
        layout3 = QHBoxLayout()

        self.drawing = QPushButton("Drawing")
        self.drawing.setCheckable(True)
        self.drawing.toggled.connect(lambda checked: self.bus.toolbox_update.emit([checked, ["Drawing","bottom_left_layout"]]))
        layout1.addWidget(self.drawing)

        self.text = QPushButton("Text")
        self.text.setCheckable(True)
        self.text.toggled.connect(lambda checked: self.bus.toolbox_update.emit([checked, ["Text","bottom_middle_widget"]]))
        layout1.addWidget(self.text)

        layout.addLayout(layout1)

        self.filters = QPushButton("Filters")
        self.filters.setCheckable(True)
        self.filters.toggled.connect(lambda checked: self.bus.toolbox_update.emit([checked, ["Filters","bottom_left_layout"]]))
        layout2.addWidget(self.filters)

        self.effects = QPushButton("Effects")
        self.effects.setCheckable(True)
        self.effects.toggled.connect(lambda checked: self.bus.toolbox_update.emit([checked, ["Effects","bottom_left_layout"]]))
        layout2.addWidget(self.effects)

        layout.addLayout(layout2)

        self.analysis = QPushButton("Analysis")
        self.analysis.setCheckable(True)
        #self.analysis.toggled.connect(lambda checked: self.bus.toolbox_update.emit([checked, ["analysis","bottom_left_layout"]]))
        layout3.addWidget(self.analysis)

        self.utility = QPushButton("Utility")
        self.utility.setCheckable(True)
        #self.utility.toggled.connect(lambda checked: self.bus.toolbox_update.emit([checked, ["effects","bottom_left_layout"]]))
        layout3.addWidget(self.utility)

        layout.addLayout(layout3)

        self.animations = QPushButton("Animations")
        self.animations.setCheckable(True)
        #self.text.toggled.connect(lambda checked: self.bus.toolbox_update.emit([checked, ["effects","bottom_left_layout"]]))
        layout.addWidget(self.animations)

        self.colors = QPushButton("Colors Manipulation")
        self.colors.setCheckable(True)
        #self.text.toggled.connect(lambda checked: self.bus.toolbox_update.emit([checked, ["effects","bottom_left_layout"]]))
        layout.addWidget(self.colors)

        self.transformations = QPushButton("Transformations")
        self.transformations.setCheckable(True)
        #self.text.toggled.connect(lambda checked: self.bus.toolbox_update.emit([checked, ["effects","bottom_left_layout"]]))
        layout.addWidget(self.transformations)

        self.setLayout(layout)

    def update_ui_configuration(self, configuration):
        print(configuration["Drawing"]["show"])
        self.bus.toolbox_update.emit([configuration["Drawing"]["show"],["Drawing","bottom_left_layout"]])
        self.drawing.setChecked(configuration["Drawing"]["show"])
        self.bus.toolbox_update.emit([configuration["Text"]["show"],["Text","bottom_middle_widget"]])
        self.text.setChecked(configuration["Text"]["show"])
        self.bus.toolbox_update.emit([configuration["Filters"]["show"],["Filters","bottom_left_layout"]])
        self.filters.setChecked(configuration["Filters"]["show"])
        self.bus.toolbox_update.emit([configuration["Effects"]["show"],["Effects","bottom_left_layout"]])
        self.effects.setChecked(configuration["Effects"]["show"])
