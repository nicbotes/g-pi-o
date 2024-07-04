import RPi.GPIO as GPIO
import time

class LED:
    def __init__(self, led_pin):
        self.led_pin = led_pin
        GPIO.setup(self.led_pin, GPIO.OUT)

    def on(self):
        GPIO.output(self.led_pin, GPIO.HIGH)

    def off(self):
        GPIO.output(self.led_pin, GPIO.LOW)
