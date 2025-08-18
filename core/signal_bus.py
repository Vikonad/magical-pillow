from PySide6.QtCore import QObject, Signal
from PySide6.QtGui import QPen

class SignalBus(QObject):
    _instance = None
    _initialized = False

    new_project = Signal(dict)
    addTab_project = Signal(dict)
    show_tab = Signal(str)
    hide_tab = Signal(str)

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(SignalBus, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not self._initialized:
            super().__init__()
            SignalBus._initialized = True
