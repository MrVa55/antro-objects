import time
from rpi_ws281x import *

# LED strip configuration:
LED_COUNT = 30        # Number of LED pixels (change this to the number of pixels in your strip)
LED_PIN = 18          # GPIO pin connected to the pixels (must support PWM!)
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10          # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False    # True to invert the signal (when using NPN transistor level shift)

# Create NeoPixel object with appropriate configuration.
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
# Intialize the library (must be called once before other functions).
strip.begin()

print('Press Ctrl-C to quit.')
try:
    while True:
        # Color all LEDs in strip
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, Color(255, 0, 0))  # Red color
        strip.show()
        time.sleep(1)

        # Turn off all LEDs
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, Color(0, 0, 0))
        strip.show()
        time.sleep(1)

except KeyboardInterrupt:
    # Turn off all LEDs on Ctrl+C
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, Color(0, 0, 0))
    strip.show()
