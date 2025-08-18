from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QComboBox, QPushButton, QHBoxLayout, QStackedWidget, QFrame
from PySide6.QtGui import QImage, QPainter, QPen, QBrush, QColor, QFont, QFontMetrics
from PySide6.QtCore import Signal, Qt, QPoint

from core import *
from .display import Display
from .photography import Photography
from .printing import Printing

class NewProjectWindow(QWidget):
    create_project = Signal(dict)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("New Project")
        self.setMinimumSize(350, 300)
        self.resize(800, 400)
        self._init_ui()

    def _init_ui(self):
        layout = QHBoxLayout()
        self.stacked_widget = QStackedWidget()

        display_tab     = QPushButton("Display")
        printing_tab    = QPushButton("Printing")
        photography_tab = QPushButton("Photography")

        display_tab.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        printing_tab.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        photography_tab.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(2))

        tabs_layout = QVBoxLayout()
        tabs_layout.addWidget(display_tab)
        tabs_layout.addWidget(printing_tab)
        tabs_layout.addWidget(photography_tab)
        tabs_layout.addStretch()

        display_content = Display()
        printing_content = Printing()
        photography_content = Photography()

        display_content.create_project.connect(self._emit_create)

        self.stacked_widget.addWidget(display_content)
        self.stacked_widget.addWidget(printing_content)
        self.stacked_widget.addWidget(photography_content)

        layout.addLayout(tabs_layout)
        layout.addWidget(self.stacked_widget)

        self.setLayout(layout)

    def _emit_create(self, project_data):
        SignalBus().new_project.emit({
            "name":project_data["name"],
            "image":self.create_image(project_data["resolution"]),
            "resolution":project_data["resolution"]
        })
        self.create_project.emit({})

    def create_image(self,resolution):
        x, y = resolution
        image = QImage(x, y, QImage.Format_ARGB32)
        image.fill(QColor("white"))
        return image
