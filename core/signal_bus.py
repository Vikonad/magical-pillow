from PySide6.QtCore import QObject, Signal
from PySide6.QtGui import QPen

class SignalBus(QObject):
    _instance = None

    # all signals are defined at the class level
    new_project = Signal(dict)
    open_image_request = Signal(str)
    open_image = Signal(str)
    layers_update_from_core = Signal(list)
    layers_update_from_ui = Signal(list)
    add_layer = Signal(str)
    addTab_project = Signal(dict)
    show_tab = Signal(str)
    hide_tab = Signal(str)
    update_ui_configuration = Signal(dict)
    toolbox_update = Signal(list)
    pen_update = Signal(QPen)
    delete_layer = Signal(str)
    send_history = Signal(dict)
    update_history = Signal(dict)

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        super().__init__()
        self._initialized = True

        #self.project_tab_switched.connect(print)

signal_bus = SignalBus()
