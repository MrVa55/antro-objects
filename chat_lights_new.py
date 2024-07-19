import json
import time
from rpi_ws281x import *

# Function to display the sequence
def display_sequence(strip, json_sequence):
    colors = json_sequence["colors"]
    while True:  # Loop to repeat the sequence
        for frame in json_sequence["sequence"]:
            frameDuration = frame["frameDuration"] / 1000.0
            ledPattern = frame["ledPattern"]
            for i in range(min(len(ledPattern), strip.numPixels())):
                color_key = ledPattern[i]
                if color_key in colors:
                    color = colors[color_key]
                    strip.setPixelColor(i, Color(color[0], color[1], color[2]))
            strip.show()
            time.sleep(frameDuration)

# Initialize the LED strip
strip = Adafruit_NeoPixel(30, 18, 800000, 10, False, 255)
strip.begin()

# Example JSON data (replace this with your actual data)
json_data = '''
{
    "colors": {
        "0": [255, 255, 0],
        "1": [0, 0, 255]
    },
    "sequence": [
        {
            "frameDuration": 500,
            "ledPattern": "000000000000000111111111111111"
        },
        {
            "frameDuration": 500,
            "ledPattern": "111111111111111000000000000000"
        }
    ]
}
'''

# Parse the JSON sequence and display it
json_sequence = json.loads(json_data)
display_sequence(strip, json_sequence)
