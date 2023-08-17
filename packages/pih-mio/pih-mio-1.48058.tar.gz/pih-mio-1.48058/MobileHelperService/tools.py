import sys
import importlib.util

pih_is_exists = importlib.util.find_spec("pih") is not None
if not pih_is_exists:
    sys.path.append("//pih/facade")
from pih import Output
from PIL import Image
import numpy as np
from DocsService.tools import Converter

class Logger:

    def __init__(self,  logger: Output, log_level: int):
        self.output = logger
        self.level = log_level

    def write_image(self, caption: str, image_object: np.ndarray | Image.Image) -> None:
        if self.level > 0:
            if isinstance(image_object, np.ndarray):
                image_object = Converter.image_array_to_image(image_object)
            self.output.write_image(
                caption, Converter.image_to_base64(image_object))

    def write_line(self, text: str) -> None:
        if self.level > 0:
            self.output.write_line(text)

    def error(self, value: str) -> None:
        if self.level > 0:
            self.output.error(value)
