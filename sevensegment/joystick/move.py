import RPi.GPIO as GPIO

class Joystick:
    def __init__(self, up_pin, down_pin, left_pin, right_pin):
        self.up_pin = up_pin
        self.down_pin = down_pin
        self.left_pin = left_pin
        self.right_pin = right_pin
        self.setup_pins()

    def setup_pins(self):
        GPIO.setup(self.up_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.down_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.left_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.right_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def read_direction(self):
        return {
            'up': not GPIO.input(self.up_pin),
            'down': not GPIO.input(self.down_pin),
            'left': not GPIO.input(self.left_pin),
            'right': not GPIO.input(self.right_pin)
        }
