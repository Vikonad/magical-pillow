import sys
from PySide6.QtWidgets import QApplication, QLabel, QMainWindow, QPushButton, QVBoxLayout, QWidget
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtCore import Qt


class Preview(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Resizable Image Viewer (QWidget + QImage)")

        # Layout
        layout = QVBoxLayout(self)
        self.setLayout(layout)

        # QLabel to hold the image
        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setMinimumSize(1, 1)
        layout.addWidget(self.label)

        self.image = QImage()

        self.resize(800, 600)

    def resizeEvent(self, event):
        """Resize image to fit widget while keeping aspect ratio."""
        if not self.image.isNull():
            scaled_img = self.image.scaled(
                self.label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
            self.label.setPixmap(QPixmap.fromImage(scaled_img))
        super().resizeEvent(event)

    def set_image(self, image):
        self.image = QImage(image)
        self.resizeEvent(None)  # force refresh
