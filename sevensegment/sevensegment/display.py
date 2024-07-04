import json
import time
import RPi.GPIO as GPIO
import os
import threading
from threading import Lock

class SevenSegmentDisplay:
    def __init__(self, config_path='config.json'):
        # Load configuration
        self.config_path = config_path
        self.load_config()
        
        # Set up GPIO
        GPIO.setmode(GPIO.BCM)
        self.setup_pins()

        # Digit patterns for numbers 0-9, A-F, and a space, with support for decimal point
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
            '9':(1,1,1,1,0,1,1,0),
            'A':(1,1,1,0,1,1,1,0),
            'b':(0,0,1,1,1,1,1,0),
            'C':(1,0,0,1,1,1,0,0),
            'd':(0,1,1,1,1,0,1,0),
            'E':(1,0,0,1,1,1,1,0),
            'F':(1,0,0,0,1,1,1,0)
        }

        # Initialize display threading
        self.display_lock = threading.Lock()
        self.current_display = '0000'
        self.keep_running = True
        self.display_thread = threading.Thread(target=self.run_display)
        self.display_thread.daemon = True
        self.display_thread.start()


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

    def run_display(self):
        while self.keep_running:
            with self.display_lock:
                self.display_number(self.current_display)
            time.sleep(0.01)  # Adjust based on testing for optimal performance

    def display_number(self, number, decimal_points=None):
        if decimal_points is None:
            decimal_points = []

        s = str(number).rjust(4)
        for digit in range(4):
            for loop in range(0, 8):
                value = self.num.get(s[digit], (0,0,0,0,0,0,0,0))[loop]
                if loop == 7 and digit in decimal_points:
                    value = 1
                GPIO.output(self.segments[loop], value)
            GPIO.output(self.digits[digit], 0)
            time.sleep(0.005)
            GPIO.output(self.digits[digit], 1)

    def update_display(self, value):
        """
        Update the display to show the given number or string, ensuring that it's
        reversed for correct display orientation.
        """
        # Convert the value to string, fill to ensure 4 characters, and reverse it
        with self.display_lock:
            reversed_value = str(value).zfill(4)[::-1]
            self.current_display = reversed_value

    def display_character(self, digit, character, decimal_point=False):
        if digit < 0 or digit > 3:
            raise ValueError("Digit must be between 0 and 3.")
        
        pattern = self.num.get(character, (0,0,0,0,0,0,0,0))
        for loop in range(0, 8):
            value = pattern[loop]
            if loop == 7 and decimal_point:
                value = 1
            GPIO.output(self.segments[loop], value)
        GPIO.output(self.digits[digit], 0)
        # time.sleep(0.001)
        GPIO.output(self.digits[digit], 1)
        GPIO.output(self.digits[digit], 1)

    def light_segment(self, digit, segment):
        if digit < 0 or digit > 3:
            raise ValueError("Digit must be between 0 and 3.")
        if segment < 0 or segment > 7:
            raise ValueError("Segment must be between 0 and 7.")
        
        GPIO.output(self.segments[segment], 1)
        GPIO.output(self.digits[digit], 0)
        # time.sleep(0.001)
        GPIO.output(self.digits[digit], 1)
        GPIO.output(self.segments[segment], 0)

    def cleanup(self):
        self.keep_running = False
        self.display_thread.join()
        for digit in range(4):
            for loop in range(0, 8):
                GPIO.output(self.segments[loop], 0)
            GPIO.output(self.digits[digit], 0)
            time.sleep(0.001)
            GPIO.output(self.digits[digit], 1)
        GPIO.cleanup()
