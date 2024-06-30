import json
import time
import RPi.GPIO as GPIO
import os

class SimpleSevenSegmentDisplay:
    def __init__(self, config_path='config.json'):
        # Load configuration
        self.config_path = config_path
        self.load_config()
        
        # Set up GPIO
        GPIO.setmode(GPIO.BCM)
        self.setup_pins()
        self.segment_numbers = {
            '0': 0,
            '1': 1,
            '2': 2,
            '3': 3,
            '4': 4,
            '5': 5,
            '6': 6,
            '7': 7,
        }
        self.digit_numbers = {
            '0': 0,
            '1': 1,
            '2': 2,
            '3': 3,
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

    def light_segment(self, digit_number, segment_number):
        if digit_number < 0 or digit_number > 3:
            raise ValueError("Digit must be between 0 and 3.")
        
        if segment_number < 0 or segment_number > 7:
            raise ValueError("Segment must be between 0 and 7.")
        
        # Get the actual GPIO pin for the segment and digit
        segment_pin = self.segments[self.segment_numbers[str(segment_number)]]
        digit_pin = self.digits[self.digit_numbers[str(digit_number)]]

        GPIO.output(segment_pin, 1)
        GPIO.output(digit_pin, 0)
        time.sleep(0.5)  # Light up the segment for 0.5 seconds
        GPIO.output(digit_pin, 1)
        GPIO.output(segment_pin, 0)

    def cleanup(self):
        # Turn off all segments
        for digit in range(4):
            for loop in range(0, 8):
                GPIO.output(self.segments[loop], 0)
            GPIO.output(self.digits[digit], 0)
            time.sleep(0.001)
            GPIO.output(self.digits[digit], 1)
        GPIO.cleanup()

def main():
    display = SimpleSevenSegmentDisplay()
    try:
        while True:
            physical_digit_number = 0  # Hardcoded to digit 0 for simplicity
            physical_segment_number = int(input("Enter the segment to illuminate (0-7): "))
            display.light_segment(physical_digit_number, physical_segment_number)
    except KeyboardInterrupt:
        display.cleanup()
    except ValueError:
        print("Invalid input. Please enter a number between 0 and 7.")
    finally:
        display.cleanup()

if __name__ == "__main__":
    main()
