import logging
from luma.oled.device import ssd1322
from luma.core.interface.serial import spi
from luma.core.render import canvas
from luma.core.virtual import terminal
from pathlib import Path
from PIL import ImageFont




class Display:
    def __init__(self):
        logging.debug("Display init")

        self._device = ssd1322(
            spi(
                bus_speed_hz=32000000,
            ), 
            width=256, 
            height=64, 
            rotate=0,
            # framebuffer="full_frame", # "diff_to_previous"
        )  # rotate=0, 1, 2 or 3 
        self._device.contrast(128)
        self._device.command(0xB3, 0xF1) 
        self._str_cache = ""

    def render(self, str):
        if str == self._str_cache: return
        self._str_cache = str

        logging.debug(f"Display rendering \"{str}\"")
        
        with canvas(self._device) as draw:
            draw.text((0, 0), str, fill="white", font_size=100)
