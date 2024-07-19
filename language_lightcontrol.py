import json
import openai
from dotenv import load_dotenv
import os
import time
from rpi_ws281x import *



# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = openai.OpenAI(api_key=os.getenv('OPENAI.API_KEY'))

def create_led_sequence(description):
    # Define the function specification for generating the LED sequence JSON
    led_sequence_function_spec = {
        "type": "function",
        "function": {
            "name": "generate_led_sequence_json",
            "description": "Create a JSON object to control an LED strip. First, define up to 9 colors, each represented by a number (0-9) and corresponding to an RGB array. Then, based on these colors, create a sequence of LED frames, each frame having a duration and a 60-character pattern string where each number corresponds to a color in the color array.",
            "parameters": {
                "type": "object",
                "properties": {
                    "colors": {
                        "type": "array",
                        "description": "An array of RGB colors, each color represented as an array of three integers (0-255). Think about which colors are good for the description",
                        "items": {
                            "type": "array",
                            "minItems": 3,
                            "maxItems": 3,
                            "items": {
                                "type": "integer",
                                "minimum": 0,
                                "maximum": 255
                            }
                        }
                    },
                    "sequence": {
                        "type": "array",
                        "description": "Array of frames for the LED sequence. Each frame consists of a duration and a 60-character string of numbers, where each number corresponds to a key in 'colors'. Try to make some imaginative and pretty sequences like rolling colors, snakes, dance moves or similar",
                        "items": {
                            "type": "object",
                            "properties": {
                                "frameDuration": {
                                    "type": "integer",
                                    "description": "Duration of the frame in milliseconds."
                                },
                                "ledPattern": {
                                    "type": "string",
                                    "description": "60-character string of numbers representing the LED pattern, where each number corresponds to a color key in 'colors'."
                                }
                            },
                            "required": ["frameDuration", "ledPattern"]
                        }
                    }
                },
                "required": ["colors", "sequence"]
            }
        }
    }


    response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=[{"role": "system", "content": "Please create an LED sequence based on this description" + description}],
        tools=[led_sequence_function_spec],
    )


    
      # Print the raw response for debugging
    # print(response)

    # Convert the response to a Python dictionary if it's a string
    response_data = json.loads(response.model_dump_json())

    # Extract the tool_calls array
    tool_calls = response_data["choices"][0]["message"]["tool_calls"]
    print(tool_calls)
    
    if tool_calls and "arguments" in tool_calls[0]["function"]:
        sequence = tool_calls[0]["function"]["arguments"]
        reason = response.choices[0].finish_reason
 

        try:
            json_sequence = json.loads(sequence)
            return json_sequence
        except json.JSONDecodeError as e:
                return f"Error in JSON format: {str(e)} Reason for stop: {reason}"
    else:
        return "Error: Expected data not found in response"

def display_sequence(strip, json_sequence):
    colors = {str(i): color for i, color in enumerate(json_sequence["colors"])}
    # colors now is like {"1": [255, 0, 0], "2": [255, 255, 255], ...}

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


# Function to configure and initialize the LED strip
def init_led_strip():
    LED_COUNT = 60
    LED_PIN = 18
    LED_FREQ_HZ = 800000
    LED_DMA = 10
    LED_BRIGHTNESS = 255
    LED_INVERT = False

    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
    strip.begin()
    return strip

# Main function to run the program
def run():
    description = input("Enter a description for the LED sequence: ")
    json_sequence = create_led_sequence(description)

    if isinstance(json_sequence, dict):
        print("Displaying the LED sequence...")
        strip = init_led_strip()
        display_sequence(strip, json_sequence)
    else:
        print("Error generating the LED sequence:", json_sequence)

if __name__ == "__main__":
    try:
        run()
    except KeyboardInterrupt:
        print("\nExiting program.")
        # Add any cleanup code here if necessary
