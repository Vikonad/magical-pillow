from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSpinBox, QColorDialog,
    QPushButton, QComboBox, QLineEdit, QDoubleSpinBox, QCheckBox
)
from PySide6.QtGui import QPen
from PySide6.QtCore import Qt

class PenSettings(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._pen = QPen()
        layout = QVBoxLayout()
        self.title = QLabel("Drawing")
        self.title.setStyleSheet('font-size: 20px; font-weight: bold;')
        layout.addWidget(self.title)
        # Color
        color_layout = QHBoxLayout()
        color_layout.addWidget(QLabel("Color:"))
        self.color_button = QPushButton()
        self.color_button.pressed.connect(self.choose_color)
        color_layout.addWidget(self.color_button)
        layout.addLayout(color_layout)

        # Opacity
        opacity_layout = QHBoxLayout()
        opacity_layout.addWidget(QLabel("Opacity:"))
        self.alpha_spin = QSpinBox()
        self.alpha_spin.setRange(0, 255)
        self.alpha_spin.setValue(self._pen.color().alpha())
        opacity_layout.addWidget(self.alpha_spin)
        layout.addLayout(opacity_layout)

        # Width
        width_layout = QHBoxLayout()
        width_layout.addWidget(QLabel("Width:"))
        self.width_spin = QSpinBox()
        self.width_spin.setRange(0, 100)
        self.width_spin.setValue(self._pen.width())
        width_layout.addWidget(self.width_spin)
        layout.addLayout(width_layout)

        # Style
        style_layout = QHBoxLayout()
        style_layout.addWidget(QLabel("Style:"))
        self.style_combo = QComboBox()
        self.styles = {
            "Solid": Qt.SolidLine,
            "Dash": Qt.DashLine,
            "Dot": Qt.DotLine,
            "Dash Dot": Qt.DashDotLine,
            "Dash Dot Dot": Qt.DashDotDotLine,
            "Custom Dash": Qt.CustomDashLine,
            "None": Qt.NoPen
        }
        self.style_combo.addItems(self.styles.keys())
        style_layout.addWidget(self.style_combo)
        layout.addLayout(style_layout)

        # Dash Pattern
        dash_layout = QHBoxLayout()
        dash_layout.addWidget(QLabel("Dash Pattern:"))
        self.dash_input = QLineEdit("4,2")
        self.dash_input.setPlaceholderText("e.g., 4,2,1,3")
        dash_layout.addWidget(self.dash_input)
        layout.addLayout(dash_layout)

        # Dash Offset
        dash_offset_layout = QHBoxLayout()
        dash_offset_layout.addWidget(QLabel("Dash Offset:"))
        self.dash_offset = QDoubleSpinBox()
        self.dash_offset.setRange(0.0, 1000.0)
        self.dash_offset.setDecimals(2)
        self.dash_offset.setValue(0.0)
        dash_offset_layout.addWidget(self.dash_offset)
        layout.addLayout(dash_offset_layout)

        # Cap Style
        cap_layout = QHBoxLayout()
        cap_layout.addWidget(QLabel("Cap:"))
        self.cap_combo = QComboBox()
        self.caps = {
            "Flat": Qt.FlatCap,
            "Square": Qt.SquareCap,
            "Round": Qt.RoundCap
        }
        self.cap_combo.addItems(self.caps.keys())
        cap_layout.addWidget(self.cap_combo)
        layout.addLayout(cap_layout)

        # Join Style
        join_layout = QHBoxLayout()
        join_layout.addWidget(QLabel("Join:"))
        self.join_combo = QComboBox()
        self.joins = {
            "Miter": Qt.MiterJoin,
            "Bevel": Qt.BevelJoin,
            "Round": Qt.RoundJoin
        }
        self.join_combo.addItems(self.joins.keys())
        join_layout.addWidget(self.join_combo)
        layout.addLayout(join_layout)

        # Miter Limit
        miter_layout = QHBoxLayout()
        miter_layout.addWidget(QLabel("Miter Limit:"))
        self.miter_limit = QDoubleSpinBox()
        self.miter_limit.setRange(0.0, 100.0)
        self.miter_limit.setDecimals(2)
        self.miter_limit.setValue(self._pen.miterLimit())
        miter_layout.addWidget(self.miter_limit)
        layout.addLayout(miter_layout)

        # Cosmetic
        self.cosmetic_checkbox = QCheckBox("Cosmetic Pen (1px regardless of zoom)")
        layout.addWidget(self.cosmetic_checkbox)


        layout.addStretch()
        self.setLayout(layout)

    def choose_color(self):
        color = QColorDialog.getColor(self._pen.color(), self)
        if color.isValid():
            color.setAlpha(self.alpha_spin.value())
            self._pen.setColor(color)
            self.update_color_button()

    def update_color_button(self):
        color = self._pen.color()
        self.color_button.setStyleSheet(f"background-color: {color.name()};")
