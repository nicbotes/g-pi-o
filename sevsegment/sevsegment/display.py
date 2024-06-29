import json
import time
import RPi.GPIO as GPIO
import os

class SevenSegmentDisplay:
    def __init__(self, config_path='config.json'):
        # Load configuration
        self.config_path = config_path
        self.load_config()
        
        # Set up GPIO
        GPIO.setmode(GPIO.BCM)
        self.setup_pins()

        # Digit patterns for numbers 0-9 and a space, with support for decimal point
        self.num = {
            ' ':(0,0,0,0,0,0,0,0),
            '0':(1,1,1,1,1,1,0,0),
            '1':(0,1,1,0,0,0,0,0),
            '2':(1,1,0,1,1,0,1,0),
            '3':(1,1,1,1,0,0,1,0),
            '4':(0,1,1,0,0,1,1,0),
            '5':(1,0,1,1,0,1,1,0),
            '6':(1,0,1,1,1,1,1,0),
            '7':(1,1,1,0,0,0,0,0),
            '8':(1,1,1,1,1,1,1,0),
            '9':(1,1,1,1,0,1,1,0)
        }

    def load_config(self):
        with open(os.path.join(os.path.dirname(__file__), self.config_path)) as config_file:
            config = json.load(config_file)
            self.segments = config['segments']
            self.digits = config['digits']

    def setup_pins(self):
        for segment in self.segments:
            GPIO.setup(segment, GPIO.OUT)
            GPIO.output(segment, 0)
        
        for digit in self.digits:
            GPIO.setup(digit, GPIO.OUT)
            GPIO.output(digit, 1)

    def display_number(self, number, decimal_points=None):
        if decimal_points is None:
            decimal_points = []

        s = str(number).rjust(4)
        for digit in range(4):
            for loop in range(0, 8):
                value = self.num[s[digit]][loop]
                if loop == 7 and digit in decimal_points:
                    value = 1
                GPIO.output(self.segments[loop], value)
            GPIO.output(self.digits[digit], 0)
            time.sleep(0.001)
            GPIO.output(self.digits[digit], 1)

    def cleanup(self):
        # Display empty segments on all digits
        for digit in range(4):
            for loop in range(0, 8):
                GPIO.output(self.segments[loop], 0)
            GPIO.output(self.digits[digit], 0)
            time.sleep(0.001)
            GPIO.output(self.digits[digit], 1)
        GPIO.cleanup()
