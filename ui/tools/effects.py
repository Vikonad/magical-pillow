from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QTabWidget, QPushButton, QScrollArea,
    QGroupBox, QGridLayout, QSizePolicy
)
from PySide6.QtCore import Qt, Signal

class Effects(QWidget):
    filter_selected = Signal(str)
    effect_selected = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setSpacing(0)
        layout.setContentsMargins(0,0,0,0)
        layout.addWidget(self._create_effects_tab())

        self.setLayout(layout)

    def _create_effects_tab(self):
        categories = {
            "Artistic / Painting Effects": ["Oil Painting", "Watercolor Effect", "Pencil Sketch", "Charcoal Drawing", "Pastel / Crayon Effect", "Ink Outline", "Comic / Cartoon Effect", "Pop Art", "Pointillism"],
            "Light and Glow Effects": ["Lens Flare", "Sun Rays / God Rays", "Glow / Bloom Effect", "Neon Glow", "Spotlight", "Glare Effect", "Light Leak"],
            "Distortion Effects": ["Ripple / Water Waves", "Twirl", "Swirl", "Pixel Stretch", "Fish-eye", "Bulge / Pinch", "Page Curl", "Mirror Warp", "Glitch / Datamosh"],
            "Texture and Pattern Effects": ["Halftone Dots", "Hatch Shading", "Paper Texture Overlay", "Canvas Texture", "Embroidery Stitch Effect", "Cracked Glass Overlay", "Snow Overlay", "Rain Effect", "Bokeh Background Blur"],
            "Color Effects": ["Gradient Map Coloring", "Duotone / Tritone", "Infrared Simulation", "Thermal Camera Effect", "Night Vision", "Sepia Variants", "Psychedelic Colors", "Color Shift Cycling"],
            "Motion and Blur Effects": ["Zoom Blur", "Spin Blur", "Directional Motion Blur", "Trails Effect", "Speed Lines"],
            "Special Stylization": ["3D Anaglyph Effect", "Chromatic Aberration", "Vaporwave Aesthetic", "Retro 8-bit Pixelation", "Stencil / Silhouette", "Double Exposure", "Tilt Shift Miniature Effect"]
        }
        return self._make_scrollable_buttons(categories, self.effect_selected)

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
