from PySide6.QtCore import QObject, Signal
from PySide6.QtGui import QColor, QPen, QImage
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

        self.bus.new_project.connect(self.create_new_project)
        self.bus.open_image.connect(self.open_image)

        self.projects = []

    def create_new_project(self, project_data):
        project = Project(name = project_data["name"])
        project.set_resolution(project_data["resolution"][0],project_data["resolution"][1])
        project.add_layer(project_data["image"], "layer 1")
        self.projects.append(project)
        project.show_project()

    def open_image(self, image_path):
        project = Project(name = image_path.split("/")[-1].split(".")[0])
        project.add_layer(QImage(image_path).convertToFormat(QImage.Format_ARGB32), "layer 1")
        self.projects.append(project)
        project.show_project()


class Project():
    def __init__(self, name):
        self.layers = []
        self.preview = ImageViewer(self.layers)
        self.name = name
        self.resolution = {}
        self.bus = SignalBus()

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
        self.bus.added_layer.emit(self.layers)

    def add_canvas(self):
        canvas = QImage(self.resolution["x"],self.resolution["y"] , QImage.Format_ARGB32)
        canvas.fill(QColor("white"))
        layer = Layer("canavs", canvas)
        self.layers.append(layer)

class Layer():
    def __init__(self, name, image):
        self.name = name
        self.image = image
