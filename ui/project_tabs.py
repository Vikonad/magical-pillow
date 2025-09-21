from PySide6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QSlider, QTextEdit, QDockWidget, QLabel, QListWidget, QVBoxLayout, QWidget, QHBoxLayout, QFrame, QListWidgetItem, QTabWidget
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QImage

from core import ProjectManager, signal_bus

class ProjectTabs(QTabWidget):
    def __init__(self):
        super().__init__()
        self.bus = signal_bus
        self.bus.addTab_project.connect(self.show_project)
        self.project_manager = ProjectManager()
        self.setTabsClosable(True)
        self.setMovable(True)
        self.currentChanged.connect(self.on_tab_changed)
        self.tabCloseRequested.connect(self.close_tab)

    def show_project(self,project):
        project["widget"].setProperty("project_id", project["id"])
        self.addTab(project["widget"], project["name"])
        self.setCurrentWidget(project["widget"])

    def close_tab(self, index):
        self.bus.close_project.emit(self.widget(index).property("project_id"))
        self.removeTab(index)

    def on_tab_changed(self, index):
        if index != -1:
            self.bus.project_tab_switched.emit(self.widget(index).property("project_id"))
