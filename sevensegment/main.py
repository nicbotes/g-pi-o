import time
import RPi.GPIO as GPIO
from led.display import LED
from joystick.move import Joystick
from ws2812.display import WS2812Display
from sevensegment.display import SevenSegmentDisplay

def main():
    # Set up GPIO pins
    button_pin = 21
    led_pin = 24
    # Joystick pins
    up_pin = 27
    down_pin = 17
    left_pin = 23
    right_pin = 22

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Button pin set as input with pull-up resistor

    led = LED(led_pin)
    joystick = Joystick(up_pin, down_pin, left_pin, right_pin)
    ws2812 = WS2812Display()
    seven_segment = SevenSegmentDisplay()

    press_count = 0
    led_position = 0  # Start LED at position 0

    try:
        last_press_time = time.time()
        last_move_time = time.time()
        while True:
            # Debounce button press
            if GPIO.input(button_pin) == GPIO.LOW and (time.time() - last_press_time) > 0.2:
                led.on()
                press_count += 1
                seven_segment.display_number(str(press_count).zfill(4))  # Display the count

                if press_count % 10 == 0:
                    ws2812.rainbow_cycle()

                last_press_time = time.time()
            else:
                led.off()

            # Joystick-controlled WS2812 LED
            direction = joystick.read_direction()
            if (time.time() - last_move_time) > 0.8:
                if direction['up'] and led_position < 23:
                    led_position += 1
                elif direction['down'] and led_position > 0:
                    led_position -= 1
                elif direction['left'] and led_position > 0:
                    led_position -= 1
                elif direction['right'] and led_position < 23:
                    led_position += 1

                ws2812.set_color(Color(0, 0, 0))  # Clear the strip
                ws2812.strip.setPixelColor(led_position, Color(255, 255, 255))  # Light only one LED
                ws2812.strip.show()
                last_move_time = time.time()

            time.sleep(0.1)  # Main loop delay

    except KeyboardInterrupt:
        GPIO.cleanup()
        ws2812.cleanup()

if __name__ == "__main__":
    main()
