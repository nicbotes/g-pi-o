#!/usr/bin/python

import time
import RPi.GPIO as GPIO
from led.display import LED
from joystick.move import Joystick
from ws2812.display import WS2812Display
from sevensegment.display import SevenSegmentDisplay
from rpi_ws281x import Color  # Import Color class
from speaker.speaker import Speaker
from threading import Thread, Lock
# from thread_control import ThreadControl

current_thread = None
lock = Lock()

def play_melody(speaker, melody_name):
    global current_thread
    with lock:
        stop_current_thread()  # Ensure any running thread is stopped before starting a new one
        current_thread = Thread(target=speaker.play_melody, args=(melody_name,))
        current_thread.start()

def play_wheel_effect(ws2812):
    global current_thread
    with lock:
        stop_current_thread()
        def wheel_effect():
            for i in range(256):  # Fast rainbow effect
                for j in range(ws2812.strip.numPixels()):
                    ws2812.strip.setPixelColor(j, ws2812.wheel((i+j) % 255))
                ws2812.strip.show()
                time.sleep(0.01)
        current_thread = Thread(target=wheel_effect)
        current_thread.start()

def stop_current_thread():
    global current_thread
    if current_thread is not None:
        current_thread.join()  # Wait for the thread to finish if it is running
    current_thread = None

def main():
#   thread_control = ThreadControl()
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)  # Disable warnings or ensure cleanup before setting modes
    button_pin = 21
    led_pin = 24

    # Joystick pins
    up_pin = 17
    down_pin = 27
    left_pin = 22
    right_pin = 23

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
    trail_1 = 23  # Start LED at position 0
    trail_2 = 22  # Start LED at position 0
    trail_3 = 21  # Start LED at position 0
    trail_4 = 20  # Start LED at position 0
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

            if GPIO.input(button_pin) == GPIO.LOW and (time.time() - last_press_time) > 0.25:
                led.on()
                press_count += 1
                count_str = str(press_count).zfill(4)
                seven_segment.update_display(count_str)

                if press_count % 10 == 0:
                    play_wheel_effect(ws2812)
                if press_count % 13 == 0:
                    play_melody(speaker, 'twinkle_twinkle')
                if press_count % 8 == 0:
                    play_melody(speaker, 'frere_jacques')

                last_press_time = time.time()
            else:
                led.off()

            direction = joystick.read_direction()
            if (time.time() - last_move_time) > 0.05:
                for dir, pressed in direction.items():
                    if pressed:
                        last_direction = dir
                        target = target_positions[dir]
                        # Determine shortest path to target
                        forward_distance = (target - led_position) % led_count
                        backward_distance = (led_position - target) % led_count

                        if forward_distance < backward_distance:
                            led_position = (led_position + 1) % led_count  # Move forward
                            trail_1 = (led_position - 1) % led_count
                            trail_2 = (led_position - 2) % led_count
                            trail_3 = (led_position - 3) % led_count
                            trail_4 = (led_position - 4) % led_count
                        else:
                            led_position = (led_position - 1) % led_count  # Move backward
                            trail_1 = (led_position + 1) % led_count # the tail leads on the backwards direction
                            trail_2 = (led_position + 2) % led_count
                            trail_3 = (led_position + 3) % led_count
                            trail_4 = (led_position + 4) % led_count # the tail is the head now.

                        break  # Exit after the first active direction is processed

                # Update LED color
                color = ws2812.wheel((color_index + led_position * 10) % 255)
                color_index = (color_index + 1) % 255

                # Clear and set new LED color
                ws2812.set_color(Color(0, 0, 0))  # Clear the strip
                ws2812.strip.setPixelColor(led_position, color)
                ws2812.strip.setPixelColor(trail_1, color)
                ws2812.strip.setPixelColor(trail_2, color)
                ws2812.strip.setPixelColor(trail_3, color)
                ws2812.strip.setPixelColor(trail_4, color)
                ws2812.strip.show()

                last_move_time = time.time()

            time.sleep(0.1)  # Main loop delay

    except KeyboardInterrupt:
        GPIO.cleanup()
        ws2812.cleanup()
        speaker.cleanup()

if __name__ == "__main__":
    main()
