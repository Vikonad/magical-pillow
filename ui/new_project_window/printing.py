import json

from PySide6.QtWidgets import QHBoxLayout, QWidget, QVBoxLayout, QLabel, QLineEdit, QComboBox, QPushButton, QFrame
from PySide6.QtCore import Qt, Signal

from .aspect_ratio_display import AspectRatioCanvas

class Printing(QWidget):
    create_project = Signal(dict)  # Send project info as a dict
    def __init__(self):
        super().__init__()
        self._init_ui()

    def _init_ui(self):
        layout = QHBoxLayout()
        self.new_project = QVBoxLayout()
        self.preview = AspectRatioCanvas()

        title = QLabel("New Project For Printing")
        title.setAlignment(Qt.AlignCenter)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Project Name")

        self.format_box = QComboBox()
        self.format_box.addItems(["RGB", "Grayscale", "CMYK"])

        self.aspect_ratio_box = QComboBox()
        self.aspect_ratio_box.addItems([
            "1:1",
        ])

        self.resolution_box = QComboBox()
        self.resolution_box.addItems([
            "1920x1920 (1:1)",
            "1280x1024 (5:4)",
            "1024x768 (4:3)",
            "1600x1200 (4:3)",
            "2560x1920 (4:3)",
            "960x720 (4:3)",
            "2160x1440 (3:2)",
            "2560x1700 (3:2)",
            "3000x2000 (3:2)",
            "1500x1000 (3:2)",
            "1280x800 (8:5)",
            "1920x1200 (8:5)",
            "2560x1600 (8:5)",
            "3840x2400 (8:5)",
            "1366x768 (16:9)",
            "1920x1080 (16:9)",
            "2560x1440 (16:9)",
            "3840x2160 (16:9)",
            "4096x2160 (256:135)",
            "2560x1080 (64:27)",
            "2440x1440 (64:27)",
            "3840x1080 (32:9)",
            "5120x1440 (32:9)",
            "17280x4320 (4:1)",
            "Custom"]
        )
        self.resolution_box.currentTextChanged.connect(
            lambda: self.preview.change_aspect_ratio(self.resolution_box.currentText().split(" ")[1][1:-1:].split(":"))
        )

        create_btn = QPushButton("Create Project")
        create_btn.clicked.connect(self._emit_create)

        self.new_project.addWidget(title)

        self.new_project.addStretch()
        self.new_project.addWidget(QLabel("Name:"))
        self.new_project.addWidget(self.name_input)

        self.new_project.addWidget(QLabel("Resolution:"))
        self.new_project.addWidget(self.resolution_box)
        self.new_project.addStretch()

        self.new_project.addWidget(create_btn)

        line = QFrame()
        line.setFrameShape(QFrame.VLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setStyleSheet("color: white; background-color: white;")
        layout.addWidget(line)
        layout.addLayout(self.new_project)
        layout.addWidget(self.preview, stretch=1)
        self.setLayout(layout)

    def resizeEvent(self, event):
        if self.width() < 400:
            self.preview.hide()
        else:
            self.preview.show()
        super().resizeEvent(event)

    def _emit_create(self, project_data):
        project_data = {
            "name": self.name_input.text(),
        #    "format": self.format_box.currentText(),
            "resolution": self.resolution_box.currentText(),
        }
        self.create_project.emit(project_data)

    def open_project_template(self):
        with open("config/default_project_formats.json") as data:
            data = json.load(data)
