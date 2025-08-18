from PySide6.QtCore import QObject, Signal
from PySide6.QtGui import QPen
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

        self.projects = []

    def create_new_project(self, project_data):
        project = Project(name = project_data["name"])
        project.set_resolution(project_data["resolution"])
        project.add_layer(project_data["image"])
        self.projects.append(project)
        project.show_project()
        print(self.projects)

class Project():
    def __init__(self, name):
        self.preview = ImageViewer()
        self.layers = []
        self.name = name
        self.resolution = [0,0]
        self.bus = SignalBus()

    def set_resolution(self, resolution):
        self.resolution = resolution

    def show_project(self):
        self.bus.addTab_project.emit({
            "name": self.name,
            "widget": self.preview
        })

    def add_layer(self, image):
        self.layers.append(image)
