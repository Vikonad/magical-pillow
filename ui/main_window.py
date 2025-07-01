from PySide6.QtWidgets import QMainWindow, QSplitter, QWidget, QTabWidget
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt

from ui import PenSettings, LayerWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Magical Pillow [DEBUG]")
        self.setMinimumSize(800, 600)

        layout = QSplitter(Qt.Horizontal)
        self.setCentralWidget(layout)

        self.left_widget = PenSettings()
        self.left_widget.setMinimumWidth(250)
        layout.addWidget(self.left_widget)

        layout.addWidget(QTabWidget())

        self.right_widget = LayerWidget()
        layout.addWidget(self.right_widget)
        self.right_widget.setMinimumWidth(250)

        layout.setSizes([150, 500, 150])

        menu_bar = self.menuBar()

        # File Menu
        file_menu = menu_bar.addMenu("File")

        # Add actions to File Menu
        new_action = QAction("New", self)
        #new_action.triggered.connect(self.new_file)
        file_menu.addAction(new_action)

        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        help_menu = menu_bar.addMenu("Edit")
        help_menu = menu_bar.addMenu("Select")
        help_menu = menu_bar.addMenu("View")
        help_menu = menu_bar.addMenu("Image")
        help_menu = menu_bar.addMenu("Layer")
        help_menu = menu_bar.addMenu("Filters")

        # Help Menu
        help_menu = menu_bar.addMenu("Help")

        about_action = QAction("About", self)
        #about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
        help_menu = menu_bar.addMenu("Help")
