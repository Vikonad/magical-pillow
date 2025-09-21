from PySide6.QtCore import QObject, Signal
from PySide6.QtGui import QColor, QPen, QImage, Qt
from PySide6.QtWidgets import QVBoxLayout, QWidget

from core import signal_bus, ImageViewer, Preview
from datetime import datetime

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

    def get_current_layer_index(self):
        layer_index = self.projects[self.current_project].image.choosenlayer
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
            self.projects[self.current_project].ui_configuration[conf[1][0]] = conf[0]

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

class Project():
    def __init__(self, name, id):
        self.bus = signal_bus
        self.id = id
        self.branches = {"master": []}
        self.choosenbranch = "master"

        self.layers = []
        self.ui_configuration = {
            "Drawing": False,
            "Text": False,
            "Filters": False,
            "Effects": False
        }
        self.image = ImageViewer(self.layers)
        self.preview = Preview()
        self.name = name
        self.resolution = {}

    def add_history(self, history):
        self.branches[self.choosenbranch].append(history)
        self.bus.update_history.emit(history)

    def update_layers(self, new_order):
        self.layers[:] = sorted(self.layers, key=lambda layer: new_order[0].index(layer.name))
        self.image.choosenlayer = next(i for i, layer in enumerate(self.layers) if layer.name == new_order[1])
        self.image.update()

    def set_resolution(self, x, y):
        self.resolution = {
            "x": x,
            "y": y
        }

    def show_project(self):
        self.bus.addTab_project.emit({
            "name": self.name,
            "widget": self.image,
            "preview": self.preview,
            "id": self.id
        })

    def delete_layer(self, layer_name):
        self.layers.remove(self.layers[self.image.choosenlayer])
        self.image.choosenlayer = len(self.layers)-1
        self.bus.layers_update_from_core.emit(self.layers)
        self.image.update()

    def add_layer(self, image, name):
        now = datetime.now()
        layer = Layer(name, image)
        if len(self.layers) == 0:
            self.set_resolution(image.width(), image.height())
            self.add_canvas()
        self.layers.append(layer)
        self.bus.layers_update_from_core.emit(self.layers)
        self.image.choosenlayer = len(self.layers)-1
        self.add_history({
            "title": "add layer",
            "parameters": {
                "image": image,
                "name": name
            },
            "date": now.strftime("%H:%M"),
            "layer": name
        })
        self.image.update()

    def add_canvas(self):
        now = datetime.now()
        canvas = QImage(self.resolution["x"],self.resolution["y"] , QImage.Format_ARGB32)
        canvas.fill(QColor("white"))
        layer = Layer("canvas", canvas)
        self.layers.append(layer)
        self.add_history({
            "title": "add canvas",
            "parameters": {
                "image": canvas,
                "name": "canvas"
            },
            "date": now.strftime("%H:%M"),
            "layer": "canvas"
        })

class Layer():
    def __init__(self, name, image):
        self.name = name
        self.image = image
