from PySide6.QtWidgets import QMainWindow, QSplitter, QVBoxLayout, QWidget, QTabWidget
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt

from ui import PenSettings, LayersWidget, HistoryWidget, ToolboxWidget, ImageViewer

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Magical Pillow [DEBUG]")
        #self.setMinimumSize(1120, 720)

        layout = QSplitter(Qt.Horizontal)
        self.setCentralWidget(layout)

        self.left_widget = QTabWidget()
        self.left_widget.setMinimumWidth(250)
        self.left_widget.setMaximumWidth(250)
        self.toolbox_layout = QSplitter(Qt.Vertical)
        self.toolbox_layout.setObjectName("mainWindow")  # Give it a name
        self.toolbox_layout.setStyleSheet("""
            QSplitter#mainWindow {
                background-color: rgb(30,30,30);
            }
        """)
        self.toolbox_layout.setContentsMargins(0,0,0,0)
        self.toolbox = ToolboxWidget()
        self.toolbox_layout.addWidget(self.toolbox)
        self.pen_settings = PenSettings()
        self.toolbox_layout.addWidget(self.pen_settings)

        self.left_widget.addTab(self.toolbox_layout, "tools")
        self.left_widget.addTab(QWidget(), "AI")

        layout.addWidget(self.left_widget)

        project_tabs = QTabWidget()
        layout.addWidget(project_tabs)

        preview = ImageViewer()

        project_tabs.addTab(preview, "preview")

        self.right_widget = QTabWidget()
        layout.addWidget(self.right_widget)
        self.right_widget.setMinimumWidth(400)
        self.right_widget.setMaximumWidth(400)

        self.layer_widget = LayersWidget()
        self.right_widget.addTab(self.layer_widget, "Layers")
        self.history_widget = HistoryWidget()
        self.right_widget.addTab(self.history_widget, "History")


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
