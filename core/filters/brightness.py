from PySide6.QtCore import QThread, Signal
from PySide6.QtWidgets import QProgressBar
from PIL import ImageEnhance

from core import ProjectManager
from utils import qimage_to_pil, pil_to_qimage

class BrightnessWorker(QThread):
    finished = Signal(object)
    progress = Signal(object)

    def __init__(self, image):
        super().__init__()
        self.project_manager = ProjectManager()
        self.image = image

    def run(self):
        result = []
        for i in range(21):
            pil_img = qimage_to_pil(self.image)
            enhancer = ImageEnhance.Brightness(pil_img)
            pil_img = enhancer.enhance(i/10)
            image = pil_to_qimage(pil_img)
            result.append(image)
            self.progress.emit(int(i/20*100))
        self.finished.emit(result)
