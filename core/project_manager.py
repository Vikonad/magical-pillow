from PySide6.QtCore import QObject, Signal
from PySide6.QtGui import QColor, QPen, QImage, Qt
from core import SignalBus
from ui.preview import ImageViewer

class ProjectManager():
    _instance = None
    _initialized = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(ProjectManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.bus = SignalBus()
        if not self._initialized:
            super().__init__()
            ProjectManager._initialized = True
        self.projects = {}
        self.current_project = 0

        self.bus.new_project.connect(self.create_new_project)
        self.bus.open_image.connect(self.open_image)
        self.bus.layers_update_from_ui.connect(self.on_layer_update)
        self.bus.project_tab_switched.connect(self.on_tab_switched)
        self.bus.toolbox_update.connect(self.on_toolbox_update)
        self.bus.add_layer.connect(self.add_layer_to_project)
        self.bus.close_project.connect(self.close_project)

    def close_project(self, project):
        item = self.projects.pop(project, None)
        if len(self.projects) == 0:
            self.bus.layers_update_from_core.emit([])

    def on_toolbox_update(self, conf):
        self.projects[self.current_project].ui_configuration[conf[1][0]] = conf[0]

    def on_tab_switched(self, tab):
        self.current_project = tab
        self.bus.layers_update_from_core.emit(self.projects[self.current_project].layers)
        self.bus.update_ui_configuration.emit(self.projects[self.current_project].ui_configuration)

    def on_layer_update(self, new_order):
        self.projects[self.current_project].update_layers(new_order)

    def create_new_project(self, project_data):
        project = Project(name = project_data["name"])
        project.set_resolution(project_data["resolution"][0],project_data["resolution"][1])
        project.add_layer(project_data["image"], "layer 1")
        self.projects[project_data["name"]] = project
        self.current_project = project_data["name"]
        project.show_project()

    def open_image(self, image_path):
        name = image_path.split("/")[-1].split(".")[0]
        project = Project(name)
        project.add_layer(QImage(image_path).convertToFormat(QImage.Format_ARGB32), "layer 1")
        self.projects[name] = project
        self.current_project = name
        project.show_project()

    def add_layer_to_project(self):
        image_resolution = self.projects[self.current_project].resolution
        image = QImage(image_resolution["x"], image_resolution["y"], QImage.Format_ARGB32)
        name = f"Layer {len(self.projects[self.current_project].layers)}"
        image.fill(Qt.transparent)
        self.projects[self.current_project].add_layer(image, name)


class Project():
    def __init__(self, name):
        self.layers = []
        self.ui_configuration = {
            "drawing": False,
            "text": False,
            "filters": False,
            "effects": False
        }
        self.preview = ImageViewer(self.layers)
        self.name = name
        self.resolution = {}
        self.bus = SignalBus()

    def update_layers(self, new_order):
        self.layers[:] = sorted(self.layers, key=lambda layer: new_order[0].index(layer.name))
        self.preview.choosenlayer = next(i for i, layer in enumerate(self.layers) if layer.name == new_order[1])
        self.preview.update()

    def set_resolution(self, x, y):
        self.resolution = {
            "x": x,
            "y": y
        }

    def show_project(self):
        self.bus.addTab_project.emit({
            "name": self.name,
            "widget": self.preview
        })

    def add_layer(self, image, name):
        layer = Layer(name, image)
        if len(self.layers) == 0:
            self.set_resolution(image.width(), image.height())
            self.add_canvas()
        self.layers.append(layer)
        self.bus.layers_update_from_core.emit(self.layers)
        self.preview.choosenlayer = len(self.layers)-1
        self.preview.update()

    def add_canvas(self):
        canvas = QImage(self.resolution["x"],self.resolution["y"] , QImage.Format_ARGB32)
        canvas.fill(QColor("white"))
        layer = Layer("canavs", canvas)
        self.layers.append(layer)

class Layer():
    def __init__(self, name, image):
        self.name = name
        self.image = image
