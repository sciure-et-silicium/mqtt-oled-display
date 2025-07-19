# https://gpiozero.readthedocs.io/en/v1.6.0/recipes.html#rotary-encoder

from threading import Event
from gpiozero import RotaryEncoder, Button

from luma.oled.device import ssd1322
from luma.core.interface.serial import spi
from luma.core.render import canvas



# Création du device SSD1322
device = ssd1322(spi(), width=256, height=64, rotate=0)  # rotate=0, 1, 2, ou 3 selon l'orientation


# Exemple d'affichage
with canvas(device) as draw:
    draw.text((10, 10), "Hello SSD1322!", fill="white", font_size=20)




rotor = RotaryEncoder(16, 20, wrap=False, max_steps=4)
btn = Button(21)
done = Event()

def rotor_to_contrast():
    value = rotor.steps
    from_low = rotor.max_steps * -1
    from_high = rotor.max_steps
    to_low = 0
    to_high = 255    
    value = max(from_low, min(value, from_high))
    return int((value - from_low) * (to_high - to_low) / (from_high - from_low) + to_low)

def on_btn_held():
    print('Exiting')
    done.set()

def on_btn_released():
    print('Btn released')

def on_rotated_clockwise():
    print('contrast up')
    print(rotor.steps)
    device.contrast(rotor_to_contrast())

def on_rotated_counter_clockwise():
    print('on_rotated_counter_clockwise')
    print(rotor.steps)
    device.contrast(rotor_to_contrast())

rotor.when_rotated_clockwise = on_rotated_clockwise
rotor.when_rotated_counter_clockwise = on_rotated_counter_clockwise

btn.when_released = on_btn_released
btn.when_held = on_btn_held

print('Hold the button to exit')
done.wait()