# https://gpiozero.readthedocs.io/en/v1.6.0/recipes.html#rotary-encoder

from threading import Event
from gpiozero import RotaryEncoder, Button

rotor = RotaryEncoder(16, 20, wrap=True, max_steps=4)
def map(value, from_low, from_high, to_low, to_high):
    # Constrain la valeur dans la plage source
    value = max(from_low, min(value, from_high))
    # Remappage
    return int((value - from_low) * (to_high - to_low) / (from_high - from_low) + to_low)



btn = Button(21)

done = Event()


def on_btn_held():
    print('Exiting')
    done.set()

def on_btn_released():
    print('Btn released')

def on_rotated_clockwise():
    print('on_rotated_clockwise')
    print(map(rotor.steps,-4,4,1,255))

def on_rotated_counter_clockwise():
    print('on_rotated_counter_clockwise')
    print(map(rotor.steps,-4,4,1,255))

rotor.when_rotated_clockwise = on_rotated_clockwise
rotor.when_rotated_counter_clockwise = on_rotated_counter_clockwise

btn.when_released = on_btn_released
btn.when_held = on_btn_held

print('Hold the button to exit')
done.wait()