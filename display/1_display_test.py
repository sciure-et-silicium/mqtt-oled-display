import time
from luma.oled.device import ssd1322
from luma.core.interface.serial import spi
from luma.core.render import canvas



# Création du device SSD1322
device = ssd1322(spi(), width=256, height=64, rotate=0)  # rotate=0, 1, 2, ou 3 selon l'orientation
device.contrast(128)



# Exemple d'affichage
with canvas(device) as draw:
    draw.text((10, 10), "Hello SSD1322!", fill="white", font_size=20)
#




time.sleep(10)