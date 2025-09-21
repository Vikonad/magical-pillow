from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PySide6.QtCore import Signal, Qt

from core import signal_bus

class StarterWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Vikonad's Magical Pillow")
        self.setFixedSize(400,350)
        self._init_ui()
        self.bus = signal_bus

    def _init_ui(self):
        layout = QVBoxLayout()

        title = QLabel("Magical Pillow")
        title.setStyleSheet("font-size: 26px; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)
        title2 = QLabel("Yet another image editing software")
        title2.setAlignment(Qt.AlignCenter)

        new_btn = QPushButton("New Project")
        open_btn = QPushButton("Open Project")

        new_btn.clicked.connect(lambda: self.bus.open_image_request.emit("new"))
        open_btn.clicked.connect(lambda: self.bus.open_image_request.emit("open"))

        layout.addWidget(title)
        layout.addWidget(title2)
        layout.addStretch()
        layout.addWidget(new_btn)
        layout.addWidget(open_btn)
        layout.addStretch()

        self.setLayout(layout)
