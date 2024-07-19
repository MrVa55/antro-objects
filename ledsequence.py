import time
import json
from rpi_ws281x import *

# LED strip configuration:
LED_COUNT = 30        # Number of LED pixels
LED_PIN = 18          # GPIO pin connected to the pixels
LED_FREQ_HZ = 800000  # LED signal frequency in hertz
LED_DMA = 10          # DMA channel to use for generating signal
LED_INVERT = False    # True to invert the signal (when using NPN transistor level shift)

# Function to create a color with brightness applied
def color_with_brightness(red, green, blue, brightness):
    return Color(int(red * brightness / 255), int(green * brightness / 255), int(blue * brightness / 255))

# Function to parse the JSON and display the sequence
def display_sequence(strip, sequence):
    for frame in sequence['ledStrip']['sequence']:
        frameDuration = frame['frameDuration'] / 1000.0  # Convert to seconds
        for state in frame['ledStates']:
            index = state['index']
            color = state['color']
            brightness = state['brightness']
            if index < strip.numPixels():
                strip.setPixelColor(index, color_with_brightness(color[0], color[1], color[2], brightness))
        strip.show()
        time.sleep(frameDuration)


# Load JSON data from a file or string
json_data = '''{
    "ledStrip": {
        "totalLEDs": 10,
        "sequence": [
            {
                "frameDuration": 500,
                "ledStates": [
                    {"index": 0, "color": [255, 0, 0], "brightness": 255},
                    {"index": 1, "color": [0, 255, 0], "brightness": 255},
                    {"index": 2, "color": [0, 0, 255], "brightness": 255},
                    {"index": 3, "color": [255, 255, 0], "brightness": 255},
                    {"index": 4, "color": [0, 255, 255], "brightness": 255},
                    {"index": 5, "color": [255, 0, 255], "brightness": 255},
                    {"index": 6, "color": [192, 192, 192], "brightness": 255},
                    {"index": 7, "color": [128, 0, 0], "brightness": 255},
                    {"index": 8, "color": [128, 128, 0], "brightness": 255},
                    {"index": 9, "color": [0, 128, 0], "brightness": 255}
                ]
            },
            {
                "frameDuration": 500,
                "ledStates": [
                    {"index": 0, "color": [0, 128, 0], "brightness": 255},
                    {"index": 1, "color": [255, 0, 0], "brightness": 255},
                    {"index": 2, "color": [0, 255, 0], "brightness": 255},
                    {"index": 3, "color": [0, 0, 255], "brightness": 255},
                    {"index": 4, "color": [255, 255, 0], "brightness": 255},
                    {"index": 5, "color": [0, 255, 255], "brightness": 255},
                    {"index": 6, "color": [255, 0, 255], "brightness": 255},
                    {"index": 7, "color": [192, 192, 192], "brightness": 255},
                    {"index": 8, "color": [128, 0, 0], "brightness": 255},
                    {"index": 9, "color": [128, 128, 0], "brightness": 255}
                ]
            }
            
        ]
    }
}
'''
sequence = json.loads(json_data)

# Create NeoPixel object with appropriate configuration.
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, 255) # Max brightness for initialization
strip.begin()

print('Press Ctrl-C to quit.')
try:
    while True:
        display_sequence(strip, sequence)
        time.sleep(1)
        # Add additional code here if you want to create more effects or patterns

except KeyboardInterrupt:
    # Turn off all LEDs on Ctrl+C
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, Color(0, 0, 0))
    strip.show()
