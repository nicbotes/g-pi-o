#!/usr/bin/python

import time

# Path to the LED's brightness control file
LED_PATH = "/sys/class/leds/ACT/brightness"

def set_led(state):
    """Set the LED state.
    Args:
        state (int): 1 to turn on, 0 to turn off.
    """
    with open(LED_PATH, 'w') as led_file:
        led_file.write(str(state))

try:
    print("Starting blinky script for built-in LED. Press Ctrl+C to exit.")
    while True:
        set_led(1)  # Turn LED on
        time.sleep(1)  # Wait for 1 second
        set_led(0)  # Turn LED off
        time.sleep(1)  # Wait for 1 second
except KeyboardInterrupt:
    print("Exiting script.")
    set_led(0)  # Ensure the LED is turned off on exit

