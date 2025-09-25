from PySide6.QtWidgets import QMainWindow, QSplitter, QVBoxLayout, QWidget, QTabWidget
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt

from ui import PenSettings, LayersWidget, HistoryWidget, ToolboxWidget, TextSettings, ProjectTabs, Filters, Effects

from core import signal_bus, ProjectManager

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.project_manager = ProjectManager()
        self.bus = signal_bus
        self.projects = []
        self.setWindowTitle("Magical Pillow [DEBUG]")
        #self.setMinimumSize(1120, 720)

        layout = QSplitter(Qt.Horizontal)
        self.setCentralWidget(layout)

        self.tab_widgets = {
            "left_widget": QTabWidget(),
            "bottom_left_layout": QTabWidget(),
            "bottom_middle_widget": QTabWidget()
        }

        self.widgets = {
            "Drawing": PenSettings(),
            "Text": TextSettings(),
            "Filters": Filters(),
            "Effects": Effects()
        }

        # left widget
        self.tab_widgets["left_widget"].setMinimumWidth(250)
        self.tab_widgets["left_widget"].setMaximumWidth(250)
        self.toolbox_layout = QVBoxLayout()
        self.toolbox_widget = QWidget()
        self.toolbox_widget.setLayout(self.toolbox_layout)
        self.tab_widgets["left_widget"].setObjectName("mainWindow")  # Give it a name
        self.tab_widgets["left_widget"].setStyleSheet("""
            QWidget#mainWindow {
                background-color: rgb(30,30,30);
            }
        """)
        self.toolbox_layout.setContentsMargins(0,0,0,0)
        self.toolbox = ToolboxWidget()
        self.bus.toolbox_update.connect(
            lambda checked:
                self.show_tab(
                    checked[1][0], checked[1][1]
                ) if checked[0] else self.hide_tab(
                    checked[1][0], checked[1][1]
            )
        )
        self.toolbox_layout.addWidget(self.toolbox)
        self.tab_widgets["bottom_left_layout"].setObjectName("penset")  # Give it a name
        self.tab_widgets["bottom_left_layout"].setStyleSheet("""
            QWidget#penset {
                background-color: rgb(30,30,30);
            }
        """)
        self.toolbox_layout.addWidget(self.tab_widgets["bottom_left_layout"])

        self.tab_widgets["left_widget"].addTab(self.toolbox_widget, "Tools")
        self.tab_widgets["left_widget"].addTab(QWidget(), "AI")

        layout.addWidget(self.tab_widgets["left_widget"])

        # middle widget
        self.middle_widget = QWidget()
        self.middle_layout = QSplitter(Qt.Vertical)
        #self.middle_widget.setLayout(self.middle_layout)

        self.tab_widgets["bottom_middle_widget"] = QTabWidget()
        self.project_tabs = ProjectTabs()
        self.middle_layout.addWidget(self.project_tabs)
        self.middle_layout.addWidget(self.tab_widgets["bottom_middle_widget"])

        layout.addWidget(self.middle_layout)

        # right widget
        self.right_widget = QTabWidget()
        layout.addWidget(self.right_widget)
        self.right_widget.setMinimumWidth(400)
        self.right_widget.setMaximumWidth(400)

        self.layer_widget = LayersWidget()
        self.right_widget.addTab(self.layer_widget, "Layers")
        self.history_widget = HistoryWidget()
        self.right_widget.addTab(self.history_widget, "History")
        self.right_widget.addTab(QWidget(), "Analysis")
        self.right_widget.addTab(QWidget(), "Utility")

        menu_bar = self.menuBar()

        # File Menu
        file_menu = menu_bar.addMenu("File")

        # Add actions to File Menu
        new_action = QAction("New", self)
        new_action.triggered.connect(lambda: self.bus.open_image_request.emit("new"))
        file_menu.addAction(new_action)

        open_action = QAction("Open", self)
        open_action.triggered.connect(lambda: self.bus.open_image_request.emit("open"))
        file_menu.addAction(open_action)

        save_action = QAction("Export", self)
        save_action.triggered.connect(lambda: self.project_manager.export_to_png())
        file_menu.addAction(save_action)

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
        help_menu.addAction(about_action)
        help_menu = menu_bar.addMenu("Help")

    def hide_tab(self, tab, tab_widget):
        if self.tab_widgets[tab_widget].indexOf(self.widgets[tab]) != -1:
            self.tab_widgets[tab_widget].removeTab(self.tab_widgets[tab_widget].indexOf(self.widgets[tab]))
        self.bus.hide_tab.emit(tab)

    def show_tab(self, tab, tab_widget):
        if self.tab_widgets[tab_widget].indexOf(self.widgets[tab]) == -1:
            self.tab_widgets[tab_widget].addTab(self.widgets[tab], tab)
            self.tab_widgets[tab_widget].setCurrentIndex(
                self.tab_widgets[tab_widget].indexOf(self.widgets[tab])
            )
        self.bus.show_tab.emit(tab)
