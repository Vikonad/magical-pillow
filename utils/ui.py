import numpy as np
from PySide6.QtGui import QImage
from PIL import Image

def clear_layout(layout):
    while layout.count():
        item = layout.takeAt(0)
        widget = item.widget()
        if widget is not None:
            widget.setParent(None)
            widget.deleteLater()
        else:
            sub_layout = item.layout()
            if sub_layout is not None:
                clear_layout(sub_layout)

def qimage_to_numpy(qimage: QImage) -> np.ndarray:
    qimage = qimage.convertToFormat(QImage.Format_ARGB32)
    width = qimage.width()
    height = qimage.height()

    ptr = qimage.bits()
    arr = np.frombuffer(ptr[: qimage.sizeInBytes()], np.uint8).reshape((height, width, 4))
    return arr.copy()

def numpy_to_qimage(arr: np.ndarray) -> QImage:
    height, width, channels = arr.shape
    bytes_per_line = channels * width
    return QImage(arr.data, width, height, bytes_per_line, QImage.Format_ARGB32).copy()

def qimage_to_pil(qimage: QImage) -> Image.Image:
    qimage = qimage.convertToFormat(QImage.Format_ARGB32)
    width, height = qimage.width(), qimage.height()
    ptr = qimage.bits()
    arr = np.frombuffer(ptr[: qimage.sizeInBytes()], np.uint8).reshape((height, width, 4)).copy()
    return Image.fromarray(arr, 'RGBA').copy()

def pil_to_qimage(pil_img: Image.Image) -> QImage:
    arr = np.array(pil_img)
    height, width, channels = arr.shape
    bytes_per_line = channels * width
    return QImage(arr.data, width, height, bytes_per_line, QImage.Format_ARGB32).copy()
