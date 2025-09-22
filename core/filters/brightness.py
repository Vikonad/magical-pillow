from PySide6.QtCore import QThread, Signal
from PIL import ImageEnhance

from core import ProjectManager
from utils import qimage_to_pil, pil_to_qimage

class BrightnessWorker(QThread):
    finished = Signal(object)  # will emit the processed QImage

    def __init__(self, image, progressbar):
        super().__init__()
        self.project_manager = ProjectManager()
        self.image = image
        self.progressbar = progressbar

    def run(self):
        self.progressbar.show()
        result = []
        for i in range(21):
            pil_img = qimage_to_pil(self.image)
            enhancer = ImageEnhance.Brightness(pil_img)
            pil_img = enhancer.enhance(i/10)
            image = pil_to_qimage(pil_img)
            result.append(image)
            self.progressbar.setValue(i/20*100)
        self.finished.emit(result)
