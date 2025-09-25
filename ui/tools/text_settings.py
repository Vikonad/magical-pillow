from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QColorDialog,
    QPushButton, QComboBox, QTextEdit, QFontComboBox, QScrollArea, QListWidget,
    QListWidgetItem
)
from PySide6.QtGui import QFontDatabase, QFont, QTextCharFormat, QTextCursor

class TextSettings(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Rich Text Editor")
        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText("Type something...")

        self.init_toolbar()

        layout = QVBoxLayout()
        layout.addLayout(self.toolbar)
        layout.addWidget(self.text_edit)
        self.setLayout(layout)

    def init_toolbar(self):
        self.toolbar = QHBoxLayout()

        # Font combo box
        self.font_box = QFontComboBox()
        self.font_box.currentFontChanged.connect(self.set_font)
        self.toolbar.addWidget(self.font_box)

        # Font size combo box
        self.size_box = QComboBox()
        self.size_box.setEditable(True)
        for i in range(8, 31, 2):
            self.size_box.addItem(str(i))
        self.size_box.setCurrentText("12")
        self.size_box.currentTextChanged.connect(self.set_font_size)
        self.toolbar.addWidget(self.size_box)

        # Bold button
        self.bold_btn = QPushButton("B")
        self.bold_btn.setCheckable(True)
        self.bold_btn.clicked.connect(self.toggle_bold)
        self.toolbar.addWidget(self.bold_btn)

        # Italic button
        self.italic_btn = QPushButton("I")
        self.italic_btn.setCheckable(True)
        self.italic_btn.clicked.connect(self.toggle_italic)
        self.toolbar.addWidget(self.italic_btn)

        # Underline button
        self.underline_btn = QPushButton("U")
        self.underline_btn.setCheckable(True)
        self.underline_btn.clicked.connect(self.toggle_underline)
        self.toolbar.addWidget(self.underline_btn)

        # Text color
        self.color_btn = QPushButton("Color")
        self.color_btn.clicked.connect(self.change_color)
        self.toolbar.addWidget(self.color_btn)

        # Background color button
        self.bgcolor_btn = QPushButton("BG Color")
        self.bgcolor_btn.clicked.connect(self.change_bg_color)
        self.toolbar.addWidget(self.bgcolor_btn)

    def merge_format_on_selection(self, format: QTextCharFormat):
        cursor = self.text_edit.textCursor()
        if not cursor.hasSelection():
            cursor.select(QTextCursor.WordUnderCursor)
        cursor.mergeCharFormat(format)

    def set_font(self, font: QFont):
        fmt = QTextCharFormat()
        fmt.setFont(font)
        self.merge_format_on_selection(fmt)

    def set_font_size(self, size):
        try:
            size = float(size)
        except ValueError:
            return
        fmt = QTextCharFormat()
        fmt.setFontPointSize(size)
        self.merge_format_on_selection(fmt)

    def toggle_bold(self):
        fmt = QTextCharFormat()
        fmt.setFontWeight(QFont.Bold if self.bold_btn.isChecked() else QFont.Normal)
        self.merge_format_on_selection(fmt)

    def toggle_italic(self):
        fmt = QTextCharFormat()
        fmt.setFontItalic(self.italic_btn.isChecked())
        self.merge_format_on_selection(fmt)

    def toggle_underline(self):
        fmt = QTextCharFormat()
        fmt.setFontUnderline(self.underline_btn.isChecked())
        self.merge_format_on_selection(fmt)

    def change_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            fmt = QTextCharFormat()
            fmt.setForeground(color)
            self.merge_format_on_selection(fmt)

    def change_bg_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            fmt = QTextCharFormat()
            fmt.setBackground(color)
            self.merge_format_on_selection(fmt)

class TextSettingsWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.theparent = parent
        self.setWindowTitle("Rich Text Editor")
        self.setMinimumHeight(500)

        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText("Type something...")

        self.init_toolbar()

        layout = QVBoxLayout()
        layout.addLayout(self.toolbar)
        layout.addWidget(self.text_edit)
        self.setLayout(layout)

    def init_toolbar(self):
        self.toolbar = QHBoxLayout()

        # Font combo box
        self.font_box = QFontComboBox()
        self.font_box.currentFontChanged.connect(self.set_font)
        self.toolbar.addWidget(self.font_box)

        # Font size combo box
        self.size_box = QComboBox()
        self.size_box.setEditable(True)
        for i in range(8, 31, 2):
            self.size_box.addItem(str(i))
        self.size_box.setCurrentText("12")
        self.size_box.currentTextChanged.connect(self.set_font_size)
        self.toolbar.addWidget(self.size_box)

        # Bold button
        self.bold_btn = QPushButton("B")
        self.bold_btn.setCheckable(True)
        self.bold_btn.clicked.connect(self.toggle_bold)
        self.toolbar.addWidget(self.bold_btn)

        # Italic button
        self.italic_btn = QPushButton("I")
        self.italic_btn.setCheckable(True)
        self.italic_btn.clicked.connect(self.toggle_italic)
        self.toolbar.addWidget(self.italic_btn)

        # Underline button
        self.underline_btn = QPushButton("U")
        self.underline_btn.setCheckable(True)
        self.underline_btn.clicked.connect(self.toggle_underline)
        self.toolbar.addWidget(self.underline_btn)

        # Text color
        self.color_btn = QPushButton("Color")
        self.color_btn.clicked.connect(self.change_color)
        self.toolbar.addWidget(self.color_btn)

        # Background color button
        self.bgcolor_btn = QPushButton("BG Color")
        self.bgcolor_btn.clicked.connect(self.change_bg_color)
        self.toolbar.addWidget(self.bgcolor_btn)


    def merge_format_on_selection(self, format: QTextCharFormat):
        cursor = self.text_edit.textCursor()
        if not cursor.hasSelection():
            cursor.select(QTextCursor.WordUnderCursor)
        cursor.mergeCharFormat(format)

    def set_font(self, font: QFont):
        fmt = QTextCharFormat()
        fmt.setFont(font)
        self.merge_format_on_selection(fmt)

    def set_font_size(self, size):
        try:
            size = float(size)
        except ValueError:
            return
        fmt = QTextCharFormat()
        fmt.setFontPointSize(size)
        self.merge_format_on_selection(fmt)

    def toggle_bold(self):
        fmt = QTextCharFormat()
        fmt.setFontWeight(QFont.Bold if self.bold_btn.isChecked() else QFont.Normal)
        self.merge_format_on_selection(fmt)

    def toggle_italic(self):
        fmt = QTextCharFormat()
        fmt.setFontItalic(self.italic_btn.isChecked())
        self.merge_format_on_selection(fmt)

    def toggle_underline(self):
        fmt = QTextCharFormat()
        fmt.setFontUnderline(self.underline_btn.isChecked())
        self.merge_format_on_selection(fmt)

    def change_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            fmt = QTextCharFormat()
            fmt.setForeground(color)
            self.merge_format_on_selection(fmt)

    def change_bg_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            fmt = QTextCharFormat()
            fmt.setBackground(color)
            self.merge_format_on_selection(fmt)
    def closeEvent(self, event):
        self.theparent.show()
        event.accept()

class FontPreviewWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Font Preview")
        self.resize(600, 800)

        main_layout = QVBoxLayout(self)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        container = QWidget()
        layout = QVBoxLayout(container)

        font_db = QFontDatabase()
        list = QListWidget()

        for font_family in font_db.families():
            label = QLabel(f"This is {font_family}")
            font = QFont(font_family)
            font.setPointSize(16)
            label.setFont(font)

            item = QListWidgetItem()
            item.setSizeHint(label.sizeHint())
            list.addItem(item)
            list.setItemWidget(item, label)

        layout.addWidget(list)

        confirm = QPushButton("Confirm font")
        confirm.setDisabled(True)
        confirm.clicked.connect(self.close)
        list.itemSelectionChanged.connect(lambda: confirm.setDisabled(False))
        layout.addWidget(confirm)

        scroll_area.setWidget(container)
        main_layout.addWidget(scroll_area)
