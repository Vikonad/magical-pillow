import numpy as np
from PIL import Image, ImageEnhance

from PySide6.QtWidgets import (
    QStackedLayout, QWidget, QVBoxLayout, QTabWidget, QPushButton, QScrollArea,
    QGroupBox, QGridLayout, QSizePolicy, QLabel, QCheckBox, QSlider
)
from PySide6.QtGui import QImage
from PySide6.QtCore import Qt

from core import signal_bus, ProjectManager
from utils import qimage_to_numpy, numpy_to_qimage, pil_to_qimage, qimage_to_pil

class Filters(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.project_manager = ProjectManager()
        self.bus = signal_bus
        layout = QVBoxLayout(self)
        layout.setSpacing(0)
        layout.setContentsMargins(0,0,0,0)
        self.selected_filter_layout = QStackedLayout()
        layout.addLayout(self.selected_filter_layout, 0)
        layout.addWidget(self._create_filters_tab(), 1)
        self.setLayout(layout)

        self.filters = [Brightness(), Contrast()]
        for filter in self.filters:
            self.selected_filter_layout.addWidget(filter)

    def _create_filters_tab(self):
        categories = {
            "Basic Adjustments": ["Brightness", "Contrast", "Saturation", "Hue Shift", "Gamma Correction", "Color balance", "Exposure correction", "White balance correction", "highlights adjustment", "Temperature"],
            "Color and Tone Filters": ["Grayscale", "Sepia", "Sepia tone", "Multitone", "Invert colors", "Solarize", "Posterize", "Threshold", "Dithering", "Colorize", "color replacement", "Color isolation", "False color mapping"],
            "Blurs": ["Gaussian Blur", "Median Blur", "Bilateral Blur", "Motion Blur", "Lens blur", "Radial blur", "Box blur"],
            "Sharpening": ["Sharpen", "Unsharp Mask", "High Pass", "Laplacian sharpening", "Clarity boost"],
            "Edge Detections": ["Sobel", "Scharr", "Canny", "Prewitt", "Roberts", "Laplacian of Gaussian", "Sketch edges"],
            "Noise Filters": ["Gaussian", "salt-and-pepper", "speckle", "Remove noise", "Grain simulation"],
            "Morphological Filters": ["Erosion", "Dilation", "Opening", "Closing", "Edge thinning", "Skeletonization"],
            "Artistic Color Filters": ["“Vintage” tone", "Warm tone", "Cold tone", "Instagram-like filters", "Cinematic teal-orange", "Cross-processing"]
        }
        return self._make_scrollable_buttons(categories)

    def _make_scrollable_buttons(self, categories):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        container = QWidget()
        container_layout = QVBoxLayout()

        item_count = 0
        for category, items in categories.items():
            group = QGroupBox(category)
            grid = QVBoxLayout()
            for i, name in enumerate(items):
                btn = QPushButton(name)
                btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
                #btn.clicked.connect(lambda checked, n=name: self.bus.filter_selected.emit(n))
                btn.clicked.connect(lambda checked, n=item_count: self.selected_filter_layout.setCurrentIndex(n))
                #btn.clicked.connect(lambda checked, n=item_count: print(self.project_manager.current_project))
                grid.addWidget(btn)
                item_count += 1
            group.setLayout(grid)
            container_layout.addWidget(group)

        container_layout.addStretch()
        container.setLayout(container_layout)
        scroll.setWidget(container)
        return scroll

class Brightness(QWidget):
    def __init__(self):
        super().__init__()
        self.bus = signal_bus
        self.project_manager = ProjectManager()
        layout = QVBoxLayout()

        self.title = QLabel("Brightness")
        self.title.setStyleSheet('font-size: 20px; font-weight: bold;')
        layout.addWidget(self.title)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(int(0.0 * int(1 / 0.1)))
        self.slider.setMaximum(int(2.0 * int(1 / 0.1)))
        self.slider.setSingleStep(1)
        self.slider.setValue(int(1.0 * int(1 / 0.1)))
        self.slider.valueChanged.connect(self.update_label)
        layout.addWidget(self.slider)

        self.label = QLabel()
        self.update_label(self.slider.value())
        layout.addWidget(self.label)

        btn = QPushButton("Confirm")
        btn.pressed.connect(self.confirm_filter)
        layout.addWidget(btn)

        preview = QCheckBox("preview")
        preview.setChecked(False)
        preview.stateChanged.connect(self.preview_mode)
        layout.addWidget(preview)
        self.setLayout(layout)

        #self.preview = QImage()

    def update_label(self, value):
        float_val = value / int(1 / 0.1)
        self.label.setText(f"Value: {float_val:.1f}")
        if len(self.project_manager.projects) != 0:
            self.apply_filter()

    def preview_mode(self, state):
        image = self.project_manager.get_current_layer()
        self.apply_filter()
        self.project_manager.preview_mode(state)

    def scale_qimage(self, image: QImage, factor: float) -> QImage:
        new_width = int(image.width() * factor)
        new_height = int(image.height() * factor)
        return image.scaled(new_width, new_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)

    def apply_filter(self):
        image = self.project_manager.get_current_layer()
        image = self.scale_qimage(image, 0.1)
        image_index = self.project_manager.get_current_layer_index()
        pil_img = qimage_to_pil(image)
        enhancer = ImageEnhance.Brightness(pil_img)
        pil_img = enhancer.enhance(self.slider.value()/10)
        image = pil_to_qimage(pil_img)
        self.project_manager.projects[self.project_manager.current_project].preview.set_image(image)
        #self.project_manager.projects[self.project_manager.current_project].preview.update()


    def confirm_filter(self):
        image = self.project_manager.get_current_layer()
        image_index = self.project_manager.get_current_layer_index()
        pil_img = qimage_to_pil(image)
        enhancer = ImageEnhance.Brightness(pil_img)
        pil_img = enhancer.enhance(self.slider.value()/10)
        image = pil_to_qimage(pil_img)
        self.project_manager.projects[self.project_manager.current_project].layers[image_index].image = image
        self.project_manager.projects[self.project_manager.current_project].image.update()
        self.project_manager.projects[self.project_manager.current_project].preview.set_image(image)

class Contrast(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        btn = QPushButton("contrast")
        layout.addWidget(btn)
        self.setLayout(layout)
