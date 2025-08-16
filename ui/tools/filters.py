from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QTabWidget, QPushButton, QScrollArea,
    QGroupBox, QGridLayout, QSizePolicy
)
from PySide6.QtCore import Qt, Signal

class Filters(QWidget):
    filter_selected = Signal(str)
    effect_selected = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setSpacing(0)
        layout.setContentsMargins(0,0,0,0)
        layout.addWidget(self._create_filters_tab())
        #layout.addWidget(self._create_effects_tab())

        self.setLayout(layout)

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
        return self._make_scrollable_buttons(categories, self.filter_selected)

    def _make_scrollable_buttons(self, categories, signal):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        container = QWidget()
        container_layout = QVBoxLayout()

        for category, items in categories.items():
            group = QGroupBox(category)
            grid = QVBoxLayout()
            for i, name in enumerate(items):
                btn = QPushButton(name)
                btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
                btn.clicked.connect(lambda checked, n=name: signal.emit(n))
                grid.addWidget(btn)  # 2 buttons per row
            group.setLayout(grid)
            container_layout.addWidget(group)

        container_layout.addStretch()
        container.setLayout(container_layout)
        scroll.setWidget(container)
        return scroll
