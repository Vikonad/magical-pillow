import sys, os

from PySide6.QtWidgets import QApplication, QFileDialog
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QIcon

from core import ProjectManager, SignalBus
from ui import MainWindow, StarterWindow
from ui.new_project_window.new_project_window import NewProjectWindow

def load_theme(app):
    with open("resources/Darkeum.qss", "r") as file:
        app.setStyleSheet(file.read())

def main():
    project_manager = ProjectManager()
    bus = SignalBus()
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("icon.png"))
    #load_theme(app)
    starter = StarterWindow()
    new_project = NewProjectWindow()
    window = MainWindow()

    def open_editor(mode: str):
        if mode == "new":
            new_project.show()

        elif mode == "open":
            file_path, _ = QFileDialog.getOpenFileName(
                starter, "Open Project", "", "Images (*.png *.jpg *.jpeg *.bmp *.gif)"
            )
            if file_path:
                file_format = os.path.splitext(file_path)[1].lower().lstrip(".")
                if file_format in ["png", "jpg"]:
                    bus.open_image.emit(file_path)
                    window.showMaximized()
                    starter.close()

    def open_main_window():
        window.showMaximized()
        starter.close()
        new_project.close()

    new_project.create_project.connect(open_main_window)
    starter.signal.connect(open_editor)

    starter.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
