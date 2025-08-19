from PySide6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QSlider, QTextEdit, QDockWidget, QLabel, QListWidget, QVBoxLayout, QWidget, QHBoxLayout, QScrollArea, QListWidgetItem
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QImage, QPixmap, QPainter, QColor

from core import SignalBus

class LayersWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.bus = SignalBus()
        self.bus.added_layer.connect(self.update_layers)
        layout = QVBoxLayout()
        self.title = QLabel("Layers")
        self.title.setStyleSheet('font-size: 20px; font-weight: bold;')
        layout.addWidget(self.title)
        layout.setSpacing(0)

        self.list = QListWidget()
        self.list.setDragDropMode(QListWidget.InternalMove)

        #image_list = [
        #    "image_samples/20231016_070401.jpg",
        #    "image_samples/20231022_104751.jpg",
        #    "image_samples/20231026_071043.jpg",
        #    "image_samples/20231110_124316.jpg",
        #    "image_samples/20231110_124334.jpg",
        #    "image_samples/20231110_124351.jpg",
        #    "image_samples/20231110_124741.jpg",
        #    "image_samples/20231110_124754.jpg",
        #    "image_samples/20231110_124834.jpg",
        #    "image_samples/20231110_124840.jpg",
        #    "image_samples/20231110_125114.jpg",
        #    "image_samples/20231110_125145.jpg",
        #    "image_samples/20231110_125244.jpg",
        #    "image_samples/20231110_125308.jpg",
        #    "image_samples/20231110_125330.jpg",
        #    "image_samples/20231110_125336.jpg",
        #    "image_samples/20231110_125342.jpg",
        #    "image_samples/20231110_125436.jpg",
        #    "image_samples/20231110_125457.jpg",
        #    "image_samples/20231026_071043.jpg",
        #    "image_samples/20231026_071043.jpg"
        #]

        self.list.setCurrentRow(0)  # Selects the second item (index starts at 0)
        bottom_buttons = QVBoxLayout()
        buttons1 = QHBoxLayout()
        up_button = QPushButton()
        buttons1.addWidget(up_button)

        down_button = QPushButton()
        buttons1.addWidget(down_button)

        delete_layer = QPushButton()
        buttons1.addWidget(delete_layer)

        bottom_buttons.addLayout(buttons1)

        self.add_new_layer = QPushButton("Add new layer")
        bottom_buttons.addWidget(self.add_new_layer)

        layout.addWidget(self.list)
        layout.addLayout(bottom_buttons)

        self.setLayout(layout)

    def update_layers(self, layers_list):
        for layer in layers_list[::-1]:
            widget = LayerWidget(layer.image, layer.name)
            widget.setContentsMargins(0, 0, 0, 0)

            item = QListWidgetItem()
            item.setSizeHint(widget.sizeHint())
            self.list.addItem(item)
            self.list.setItemWidget(item, widget)

class LayerWidget(QWidget):
    def __init__(self, image, title):
        super().__init__()
        layout = QHBoxLayout()
        layout.setSpacing(3)
        layout.setContentsMargins(0, 0, 0, 0)

        source_image = QImage(image)
        white_bg = QImage(70, 70, QImage.Format_ARGB32)
        white_bg.fill(QColor(30,30,30))
        painter = QPainter(white_bg)
        scaled = source_image.scaled(70, 70, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        x = (70 - scaled.width()) // 2
        y = (70 - scaled.height()) // 2
        painter.drawImage(x, y, scaled)
        painter.end()
        pixmap = QPixmap.fromImage(white_bg)
        label = QLabel()
        label.setFixedSize(70,70)
        label.setPixmap(pixmap)
        button = QLabel(title)
        button.setStyleSheet("font-size: 15px;")
        button.setAlignment(Qt.AlignCenter)
        button.setMinimumHeight(75)
        layout.addWidget(label)
        layout.addWidget(button)
        self.setLayout(layout)
