import RPi.GPIO as GPIO
import time

# Set up the GPIO mode
GPIO.setmode(GPIO.BCM)

# Define the GPIO pins for the joystick
up_pin = 17
down_pin = 27
left_pin = 22
right_pin = 23

# Set up the GPIO pins as inputs
GPIO.setup(up_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(down_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(left_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(right_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

try:
    while True:
        if not GPIO.input(up_pin):
            print("Up pressed")
        if not GPIO.input(down_pin):
            print("Down pressed")
        if not GPIO.input(left_pin):
            print("Left pressed")
        if not GPIO.input(right_pin):
            print("Right pressed")
        time.sleep(0.1)
except KeyboardInterrupt:
    GPIO.cleanup()

