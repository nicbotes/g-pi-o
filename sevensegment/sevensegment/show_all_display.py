import json
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

    def load_config(self):
        with open(os.path.join(os.path.dirname(__file__), self.config_path)) as config_file:
            config = json.load(config_file)
            self.segments = config['segments']
            self.digits = config['digits']

    def setup_pins(self):
        for segment in self.segments:
            GPIO.setup(segment, GPIO.OUT)
            GPIO.output(segment, GPIO.LOW)  # Set all segments to HIGH (off)
            print("setup: ", segment, " ", GPIO.LOW)
        
        for digit in self.digits:
            GPIO.setup(digit, GPIO.OUT)
            GPIO.output(digit, GPIO.HIGH)  # Set all digits to HIGH (off)
            print("setup Digp: ", digit, " ", GPIO.HIGH)

    def cleanup(self):
        # Turn off all segments and digits
        for segment in self.segments:
            GPIO.output(segment, GPIO.HIGH)
        for digit in self.digits:
            GPIO.output(digit, GPIO.HIGH)
        GPIO.cleanup()

def main():
    display = SimpleSevenSegmentDisplay()
    try:
        print("All segments and digits should now be off.")
        input("Press Enter to exit...")
    except KeyboardInterrupt:
        pass
    finally:
        display.cleanup()

if __name__ == "__main__":
    main()

