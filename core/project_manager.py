from PySide6.QtCore import QObject, Signal, QSize
from PySide6.QtGui import QColor, QPen, QImage, Qt, QPainter
from PySide6.QtWidgets import QVBoxLayout, QWidget

from core import signal_bus, ImageViewer, Preview, Project

class ProjectManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return  # skip re-initialization
        self._initialized = True

        self._next_id = 1
        self.bus = signal_bus
        self.projects = {}
        self.current_project = 0

        self.bus.new_project.connect(self.create_new_project)
        self.bus.open_image.connect(self.open_image)
        self.bus.layers_update_from_ui.connect(self.on_layer_update)
        self.bus.toolbox_update.connect(self.on_toolbox_update)
        self.bus.add_layer.connect(self.add_layer_to_project)
        self.bus.send_history.connect(self.send_history)
        self.bus.delete_layer.connect(self.delete_layer)

        self.filters_cache = []

    def export_to_png(self):
        layers = self.get_current_project().layers
        if not layers:
            return None

        # Use the size of the first image as canvas size
        width = layers[0].image.width()
        height = layers[0].image.height()
        result = QImage(QSize(width, height), QImage.Format_ARGB32)
        result.fill(0)  # Transparent background

        painter = QPainter(result)
        for layer in layers:
            painter.drawImage(0, 0, layer.image)  # Draw each layer at top-left corner
        painter.end()
        result.save("merged.jpg")

    def get_current_project(self):
        return self.projects[self.current_project]

    def get_current_layer_index(self):
        layer_index = self.get_current_project().image.choosenlayer
        return layer_index

    def get_current_layer(self):
        image = self.projects[self.current_project].layers[self.get_current_layer_index()].image
        return image

    def delete_layer(self, layer_id):
        if len(self.projects) >= 1:
            self.projects[self.current_project].delete_layer(layer_id)

    def send_history(self, history):
        self.projects[self.current_project].add_history(history)

    def close_project(self, project):
        item = self.projects.pop(project, None)
        if len(self.projects) == 0:
            self.bus.layers_update_from_core.emit([])

    def on_toolbox_update(self, conf):
        if len(self.projects) >= 1:
            self.projects[self.current_project].ui_configuration[conf[1][0]]["show"] = conf[0]

    def on_tab_switched(self, tab):
        self.current_project = tab
        self.bus.layers_update_from_core.emit(self.projects[self.current_project].layers)
        self.bus.update_ui_configuration.emit(self.projects[self.current_project].ui_configuration)

    def on_layer_update(self, new_order):
        self.projects[self.current_project].update_layers(new_order)

    def create_new_project(self, project_data):
        project = Project(project_data["name"], self._next_id)
        project.set_resolution(project_data["resolution"][0],project_data["resolution"][1])
        project.add_layer(project_data["image"], "layer 1")
        self.projects[project.id] = project
        self.current_project = project.id
        project.show_project()
        self._next_id += 1

    def open_image(self, image_path):
        name = image_path.split("/")[-1].split(".")[0]
        project = Project(name, self._next_id)
        project.add_layer(QImage(image_path).convertToFormat(QImage.Format_ARGB32), "layer 1")
        self.projects[project.id] = project
        self.current_project = project.id
        project.show_project()
        self._next_id += 1

    def add_layer_to_project(self):
        if len(self.projects) >= 1:
            image_resolution = self.projects[self.current_project].resolution
            image = QImage(image_resolution["x"], image_resolution["y"], QImage.Format_ARGB32)
            name = f"Layer {len(self.projects[self.current_project].layers)}"
            image.fill(Qt.transparent)
            self.projects[self.current_project].add_layer(image, name)

    def preview_mode(self, arg):
        if arg:
            self.projects[self.current_project].image.hide()
            self.projects[self.current_project].preview.show()
        else:
            self.projects[self.current_project].image.show()
            self.projects[self.current_project].preview.hide()
