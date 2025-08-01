import sys

from PySide6.QtWidgets import QApplication, QFileDialog
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QIcon

from ui import MainWindow, StarterWindow
from ui.new_project_window.new_project_window import NewProjectWindow

def load_theme(app):
    with open("resources/Darkeum.qss", "r") as file:
        app.setStyleSheet(file.read())

def main():
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("icon.png"))  # or .ico on Windows
    #load_theme(app)
    starter = StarterWindow()
    new_project = NewProjectWindow()
    window = MainWindow()

    def open_editor(mode: str):
        if mode == "new":
            window.showMaximized()
            new_project.show()
            #window.new_file()
            starter.close()

        elif mode == "open":
            file_path, _ = QFileDialog.getOpenFileName(
                starter, "Open Project", "", "Images (*.png *.jpg *.jpeg *.bmp *.gif)"
            )
            if file_path:
                window.showMaximized()
                starter.close()

    starter.signal.connect(open_editor)

    starter.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
