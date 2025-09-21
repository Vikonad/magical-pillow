import sys
from PySide6.QtWidgets import QApplication, QLabel, QMainWindow, QPushButton, QVBoxLayout, QWidget
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt


class Preview(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Resizable Image Viewer")

        central = QWidget(self)
        layout = QVBoxLayout(central)
        self.setCentralWidget(central)

        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setMinimumSize(1, 1)
        layout.addWidget(self.label)

        self.button = QPushButton("Change Image", self)
        self.button.clicked.connect(self.change_image)
        layout.addWidget(self.button)

        self.pixmap = QPixmap()
        self.resize(800, 600)

    def resizeEvent(self, event):
        if not self.pixmap.isNull():
            scaled_pixmap = self.pixmap.scaled(
                self.label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
            self.label.setPixmap(scaled_pixmap)
        super().resizeEvent(event)

    def set_image(self, path: str):
        self.pixmap = QPixmap(path)
        self.resizeEvent(None)

    def change_image(self):
        self.set_image("another_image.jpg")  # put a valid image path
