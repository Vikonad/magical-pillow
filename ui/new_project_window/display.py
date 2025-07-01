import json

from PySide6.QtWidgets import QHBoxLayout, QWidget, QVBoxLayout, QLabel, QLineEdit, QComboBox, QPushButton, QFrame
from PySide6.QtCore import Qt, Signal

from .open_format_file import open_file
from .aspect_ratio_display import AspectRatioCanvas

class Display(QWidget):
    create_project = Signal(dict)  # Send project info as a dict
    def __init__(self):
        super().__init__()

        self.data = open_file()["display"]

        self.current_aspect_ratio = ""
        self.current_resolution = ""

        self._init_ui()

    def _init_ui(self):
        layout = QHBoxLayout()
        self.new_project = QVBoxLayout()
        self.preview = AspectRatioCanvas()

        self.title = QLabel("New Project For Display")
        self.title.setStyleSheet('font-size: 24px; font-weight: bold;')
        self.title.setAlignment(Qt.AlignCenter)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Project Name")

        self.format_box = QComboBox()
        self.format_box.addItems(["RGB", "Grayscale", "CMYK"])

        self.aspect_ratio_box = QComboBox()
        self.resolution_box = QComboBox()

        self.aspect_ratio_template()
        self.resolution_template()

        create_btn = QPushButton("Create Project")
        create_btn.clicked.connect(self._emit_create)

        self.new_project.addWidget(self.title)

        self.new_project.addStretch()
        self.new_project.addWidget(QLabel("Name:"))
        self.new_project.addWidget(self.name_input)

        self.new_project.addWidget(QLabel("Aspect ratio:"))
        self.new_project.addWidget(self.aspect_ratio_box)

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
        if self.width() < 600:
            self.preview.hide()
            self.title.hide()
        else:
            self.preview.show()
            self.title.show()
        super().resizeEvent(event)

    def _emit_create(self, project_data):
        project_data = {
            "name": self.name_input.text(),
            "aspect_ratio": self.current_aspect_ratio,
            "resolution": self.current_resolution,
        }
        self.create_project.emit(project_data)

    def aspect_ratio_template(self):
        for tp in self.data:
            #print(tp)
            for ar in self.data[tp]:
                print(ar)
                self.aspect_ratio_box.addItem(
                    ar + ' (' + self.data[tp][ar]["description"] + ')', ar
                )
        self.current_aspect_ratio = self.aspect_ratio_box.itemData(self.aspect_ratio_box.currentIndex())
        self.aspect_ratio_box.currentTextChanged.connect(self.on_aspect_ratio_changed)
        self.resolution_template()

    def resolution_template(self):
        self.resolution_box.clear()
        for e in self.data["Comuter/Monitor"][self.current_aspect_ratio]["resolutions"]:
            self.resolution_box.addItem(
                e["description"],[e["x"],e["y"]]
            )
        self.current_resolution = self.resolution_box.itemData(self.resolution_box.currentIndex())

    def on_aspect_ratio_changed(self):
        self.current_aspect_ratio = self.aspect_ratio_box.itemData(self.aspect_ratio_box.currentIndex())
        self.preview.change_aspect_ratio(
            self.aspect_ratio_box.itemData(
                self.aspect_ratio_box.currentIndex()
            ).split(":")
        )
        self.resolution_template()
