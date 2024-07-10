#!/usr/bin/python

import time
import RPi.GPIO as GPIO
from led.display import LED
from joystick.move import Joystick
from ws2812.display import WS2812Display
from sevensegment.display import SevenSegmentDisplay
from rpi_ws281x import Color  # Import Color class
from speaker.speaker import Speaker

def main():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)  # Disable warnings or ensure cleanup before setting modes
    button_pin = 21
    led_pin = 24

    # Joystick pins
    up_pin = 27
    down_pin = 17
    left_pin = 23
    right_pin = 22

    # ws2812
    led_count = 24

    GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Button pin set as input with pull-up resistor

    speaker_pin = 12
    speaker = Speaker(speaker_pin)  # Initialize speaker on GPIO 12

    led = LED(led_pin)
    joystick = Joystick(up_pin, down_pin, left_pin, right_pin)
    ws2812 = WS2812Display()
    seven_segment = SevenSegmentDisplay()

    press_count = 0
    led_position = 0  # Start LED at position 0
    color_index = 0   # Start color index for rainbow

    target_positions = {
        'right': 6,
        'down': 12,
        'left': 18,
        'up': 0
    }

    try:
        last_press_time = time.time()
        last_move_time = time.time()
        while True:
            # Display reversed count on seven-segment
            count_str = str(press_count).zfill(4)
            seven_segment.update_display(count_str)

            if GPIO.input(button_pin) == GPIO.LOW and (time.time() - last_press_time) > 0.5:
                led.on()
                press_count += 1
                count_str = str(press_count).zfill(4)
                seven_segment.update_display(count_str)

                if press_count % 10 == 0:
                    for i in range(256):  # Fast rainbow effect
                        for j in range(ws2812.strip.numPixels()):
                            ws2812.strip.setPixelColor(j, ws2812.wheel((i+j) % 255))
                        ws2812.strip.show()
                        time.sleep(0.01)
                if press_count % 13 == 0:
                    speaker.play_melody('twinkle_twinkle')
                if press_count % 8 == 0:
                    speaker.play_melody('frere_jacques')

                last_press_time = time.time()
            else:
                led.off()

            direction = joystick.read_direction()
            if (time.time() - last_move_time) > 0.2:
                for dir, pressed in direction.items():
                    if pressed:
                        target = target_positions[dir]
                        # Determine shortest path to target
                        forward_distance = (target - led_position) % led_count
                        backward_distance = (led_position - target) % led_count

                        if forward_distance < backward_distance:
                            led_position = (led_position + 1) % led_count  # Move forward
                        else:
                            led_position = (led_position - 1) % led_count  # Move backward

                        break  # Exit after the first active direction is processed

                # Update LED color
                color = ws2812.wheel((color_index + led_position * 10) % 255)
                color_index = (color_index + 1) % 255

                # Clear and set new LED color
                ws2812.set_color(Color(0, 0, 0))  # Clear the strip
                ws2812.strip.setPixelColor(led_position, color)
                ws2812.strip.show()

                last_move_time = time.time()

            time.sleep(0.1)  # Main loop delay

    except KeyboardInterrupt:
        GPIO.cleanup()
        ws2812.cleanup()
        speaker.cleanup()

if __name__ == "__main__":
    main()
