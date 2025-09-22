from PySide6.QtGui import QColor, QPen, QImage, Qt

from core import signal_bus, ImageViewer, Preview, Layer
from datetime import datetime

class Project():
    def __init__(self, name, id):
        self.filters_cache_ready = False
        self.filters_cache = []

        self.bus = signal_bus
        self.id = id
        self.branches = {"master": []}
        self.choosenbranch = "master"

        self.layers = []
        self.ui_configuration = {
            "Drawing": {
                "show": False
            },
            "Text": {
                "show": False
            },
            "Filters": {
                "show": False,
                "selected-filter": -1,
                "configurations": {}
            },
            "Effects": {
                "show": False
            }
        }
        self.image = ImageViewer(self.layers)
        self.preview = Preview()
        self.preview.hide()
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
            "image": self.image,
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
