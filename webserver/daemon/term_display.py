import logging
from luma.oled.device import ssd1322
from luma.core.interface.serial import spi
from luma.core.render import canvas
from luma.core.virtual import terminal
from pathlib import Path
from PIL import ImageFont



def make_font(name, size):
    font_path = str(Path(__file__).resolve().parent.joinpath('fonts', name))
    logging.debug(f"Loading font {font_path}")
    return ImageFont.truetype(font_path, size)


#[
#    (None, None), 
#    ("tiny.ttf", 6), 
#    ("ProggyTiny.ttf", 16), # bien !
#    ("creep.bdf", 16), 
#    ("miscfs_.ttf", 12), # bien !
#    ("FreePixel.ttf", 12), # bien !
#    ('ChiKareGo.ttf', 16)
#]

# font = make_font(fontname, size) if fontname else None
# term = terminal(device, font)


class TermDisplay:
    def __init__(self):
        logging.debug("Display init")

        self._device = ssd1322(
            spi(
                bus_speed_hz=32000000,
            ), 
            width=256, 
            height=64, 
            rotate=0,
        )  # rotate=0, 1, 2 or 3 
        font = make_font("ProggyTiny.ttf", 16) 
        self._term = terminal(self._device, font)

        self._device.contrast(128)
        self._str_cache = ""

    def render(self, str):
        if str == self._str_cache: return
        self._str_cache = str

        logging.debug(f"Display rendering \"{str}\"")
        self._term.println(str)

        #with canvas(self._device) as draw:
        #    draw.text((0, 0), str, fill="white", font_size=100)
