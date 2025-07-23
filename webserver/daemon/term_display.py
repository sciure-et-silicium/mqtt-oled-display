import logging
from luma.oled.device import ssd1322
from luma.core.interface.serial import spi
from luma.core.render import canvas
from luma.core.virtual import terminal
from pathlib import Path
from PIL import ImageFont

FONTS = [
    ["FreePixel.ttf", 12],
    ["miscfs_.ttf", 12],
    ["ProggyTiny.ttf", 16],
]

def make_font(id):
    name = FONTS[id][0]
    size = FONTS[id][1]

    font_path = str(Path(__file__).resolve().parent.joinpath('fonts', name))
    logging.debug(f"Loading font {font_path}")
    return ImageFont.truetype(font_path, size)


class TermDisplay:
    def __init__(self):
        logging.debug("Display init")

        self._device = ssd1322(spi(), width=256, height=64, rotate=0)

        font = make_font(1) 
        self._term = terminal(self._device, font)
        self._device.contrast(128)
        self._str_cache = ""

    def render(self, str):
        if str == self._str_cache: return
        self._str_cache = str

        logging.debug(f"Display rendering \"{str}\"")
        self._term.println(str)