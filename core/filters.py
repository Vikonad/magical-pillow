import numpy as np
from PIL import Image

from core import SignalBus

# Increase brightness by adding a constant
brightness = 40
bright_img = np.clip(img + brightness, 0, 255).astype(np.uint8)

Image.fromarray(bright_img).save("brighter.jpg")
