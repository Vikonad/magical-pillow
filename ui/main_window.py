from PySide6.QtWidgets import QMainWindow, QSplitter, QVBoxLayout, QWidget, QTabWidget, QStackedWidget
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt

from ui import PenSettings, LayersWidget, HistoryWidget, ToolboxWidget, ImageViewer, TextSettings
from ui.tools.filters import Filters
from ui.tools.effects import Effects

from core import SignalBus

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.bus = SignalBus()
        self.projects = []
        self.bus.addTab_project.connect(self.show_project)
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
        self.tab_widgets["left_widget"] = QTabWidget()
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
        self.project_tabs = QTabWidget()
        self.project_tabs.setTabsClosable(True)
        self.project_tabs.setMovable(True)
        self.project_tabs.currentChanged.connect(self.on_tab_changed)
        self.project_tabs.tabCloseRequested.connect(self.close_tab)
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

        open_action = QAction("Open", self)
        open_action.triggered.connect(lambda: self.bus.open_image_request.emit("open"))
        file_menu.addAction(new_action)
        file_menu.addAction(open_action)

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

    def show_project(self,project):
        project["widget"].setProperty("project_id", project["id"])
        self.project_tabs.addTab(project["widget"], project["name"])
        self.project_tabs.setCurrentWidget(project["widget"])

    def close_tab(self, index):
        self.bus.close_project.emit(self.project_tabs.widget(index).property("project_id"))
        self.project_tabs.removeTab(index)

    def on_tab_changed(self, index):
        if index != -1:
            self.bus.project_tab_switched.emit(self.project_tabs.widget(index).property("project_id"))
