import RPi.GPIO as GPIO
import time

# Set up GPIO mode
GPIO.setmode(GPIO.BCM)

# Set up GPIO pins
button_pin = 21
led_pin = 24

GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Button pin set as input with pull-up resistor
GPIO.setup(led_pin, GPIO.OUT)  # LED pin set as output

try:
    while True:
        button_state = GPIO.input(button_pin)
        if button_state == GPIO.LOW:  # Button is pressed (assuming active low)
            GPIO.output(led_pin, GPIO.HIGH)  # Turn LED on
        else:
            GPIO.output(led_pin, GPIO.LOW)  # Turn LED off
        time.sleep(0.1)  # Small delay to debounce

except KeyboardInterrupt:
    GPIO.cleanup()  # Clean up GPIO on CTRL+C exit

