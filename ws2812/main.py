import time
from rpi_ws281x import PixelStrip, Color

# LED strip configuration:
LED_COUNT = 24        # Number of LED pixels.
LED_PIN = 18          # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10          # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False    # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0       # PWM channel

# Create PixelStrip object
strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
strip.begin()

def set_color(strip, color):
    """Set all pixels in the strip to the specified color."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
    strip.show()

def color_wipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms / 1000.0)

def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)

def rainbow_cycle(strip, wait_ms=20, iterations=5):
    """Draw rainbow that uniformly distributes itself across all pixels."""
    for j in range(256 * iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((i * 256 // strip.numPixels() + j) & 255))
        strip.show()
        time.sleep(wait_ms / 1000.0)

try:
    print("Color wipe red")
    color_wipe(strip, Color(255, 0, 0))  # Red wipe
    time.sleep(1)
    print("Color wipe green")
    color_wipe(strip, Color(0, 255, 0))  # Green wipe
    time.sleep(1)
    print("Color wipe blue")
    color_wipe(strip, Color(0, 0, 255))  # Blue wipe
    time.sleep(1)
    print("Rainbow cycle")
    rainbow_cycle(strip)  # Rainbow cycle

except KeyboardInterrupt:
    pass
finally:
    # Turn off the LEDs
    set_color(strip, Color(0, 0, 0))
    print("LEDs should be off now.")

