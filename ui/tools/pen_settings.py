from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSpinBox, QColorDialog,
    QPushButton, QComboBox, QLineEdit, QDoubleSpinBox
)
from PySide6.QtGui import QPen
from PySide6.QtCore import Qt

from core import signal_bus

class PenSettings(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.bus = signal_bus
        self._pen = QPen()
        layout = QVBoxLayout(self)
        self.title = QLabel("Drawing")
        self.title.setStyleSheet('font-size: 20px; font-weight: bold;')
        layout.addWidget(self.title)

        # Color
        color_layout = QHBoxLayout()
        color_layout.addWidget(QLabel("Color:"))
        self.color_button = QPushButton()
        self.color_button.clicked.connect(self.choose_color)
        color_layout.addWidget(self.color_button)

        layout.addLayout(color_layout)

        # Width
        width_layout = QHBoxLayout()
        width_layout.addWidget(QLabel("Width:"))
        self.width_spin = QSpinBox()
        self.width_spin.setRange(0, 100)
        self.width_spin.setValue(self._pen.width())
        self.width_spin.valueChanged.connect(self.update_pen)
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
        self.style_combo.currentIndexChanged.connect(self.update_pen)
        style_layout.addWidget(self.style_combo)
        layout.addLayout(style_layout)

        # Dash Pattern
        dash_layout = QHBoxLayout()
        dash_layout.addWidget(QLabel("Dash Pattern:"))
        self.dash_input = QLineEdit("4,2")
        self.dash_input.setPlaceholderText("e.g., 4,2,1,3")
        self.dash_input.textChanged.connect(self.update_pen)
        dash_layout.addWidget(self.dash_input)
        layout.addLayout(dash_layout)

        # Dash Offset
        dash_offset_layout = QHBoxLayout()
        dash_offset_layout.addWidget(QLabel("Dash Offset:"))
        self.dash_offset = QDoubleSpinBox()
        self.dash_offset.setRange(0.0, 1000.0)
        self.dash_offset.setDecimals(2)
        self.dash_offset.setValue(0.0)
        self.dash_offset.valueChanged.connect(self.update_pen)
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
        self.cap_combo.currentIndexChanged.connect(self.update_pen)
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
        self.join_combo.currentIndexChanged.connect(self.update_pen)
        join_layout.addWidget(self.join_combo)
        layout.addLayout(join_layout)

        # Miter Limit
        miter_layout = QHBoxLayout()
        miter_layout.addWidget(QLabel("Miter Limit:"))
        self.miter_limit = QDoubleSpinBox()
        self.miter_limit.setRange(0.0, 100.0)
        self.miter_limit.setDecimals(2)
        self.miter_limit.setValue(self._pen.miterLimit())
        self.miter_limit.valueChanged.connect(self.update_pen)
        miter_layout.addWidget(self.miter_limit)
        layout.addLayout(miter_layout)

        layout.addStretch()

    def choose_color(self):
        color = QColorDialog.getColor(self._pen.color(), self)
        if color.isValid():
            self._pen.setColor(color)
            self.update_color_button()
            self.bus.pen_update.emit(self._pen)

    def update_color_button(self):
        color = self._pen.color()
        self.color_button.setStyleSheet(f"background-color: {color.name()};")

    def update_pen(self):
        color = self._pen.color()
        self._pen.setColor(color)
        self._pen.setWidth(self.width_spin.value())
        self._pen.setStyle(self.styles[self.style_combo.currentText()])
        self._pen.setCapStyle(self.caps[self.cap_combo.currentText()])
        self._pen.setJoinStyle(self.joins[self.join_combo.currentText()])
        self._pen.setMiterLimit(self.miter_limit.value())
        self._pen.setDashOffset(self.dash_offset.value())

        # Custom Dash Pattern
        if self._pen.style() == Qt.CustomDashLine:
            try:
                pattern = [float(x.strip()) for x in self.dash_input.text().split(",") if x.strip()]
                if pattern:
                    self._pen.setDashPattern(pattern)
            except ValueError:
                pass  # Ignore invalid input

        self.update_color_button()
        self.bus.pen_update.emit(self._pen)

    def setPen(self, pen: QPen):
        self._pen = QPen(pen)  # Make a copy
        self.width_spin.setValue(pen.width())
        self.color_button.setStyleSheet(f"background-color: {pen.color().name()};")

        self.style_combo.setCurrentText(self._style_name(pen.style()))
        self.cap_combo.setCurrentText(self._cap_name(pen.capStyle()))
        self.join_combo.setCurrentText(self._join_name(pen.joinStyle()))

        self.dash_offset.setValue(pen.dashOffset())
        self.miter_limit.setValue(pen.miterLimit())

        if pen.style() == Qt.CustomDashLine:
            self.dash_input.setText(", ".join(str(d) for d in pen.dashPattern()))

    def pen(self) -> QPen:
        return self._pen

    def _style_name(self, style):
        for name, value in self.styles.items():
            if value == style:
                return name
        return "Solid"

    def _cap_name(self, cap):
        for name, value in self.caps.items():
            if value == cap:
                return name
        return "Flat"

    def _join_name(self, join):
        for name, value in self.joins.items():
            if value == join:
                return name
        return "Miter"
