from PySide6.QtCore import QObject, Signal
from PySide6.QtGui import QPen

class SignalBus(QObject):
    _instance = None
    _initialized = False

    new_project = Signal(dict)
    open_image_request = Signal(str)
    open_image = Signal(str)
    layers_update_from_core = Signal(list)
    layers_update_from_ui = Signal(list)
    addTab_project = Signal(dict)
    show_tab = Signal(str)
    hide_tab = Signal(str)
    project_tab_switched = Signal(str)
    update_ui_configuration = Signal(dict)
    toolbox_update = Signal(list)

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(SignalBus, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not self._initialized:
            super().__init__()
            SignalBus._initialized = True
