import keyboard

# https://www.cnpython.com/qa/372750
def print_pressed_keys(e):
    line = ', '.join(str(code) for code in keyboard._pressed_events)
    print(line)


keyboard.hook(print_pressed_keys)
keyboard.wait()

