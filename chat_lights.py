import json
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(api_key=os.getenv('OPENAI.API_KEY'))  # Ensure the environment variable matches your .env file

def create_led_sequence(description):
    json_format_description = (
        "Generate a JSON sequence for controlling WS2812B LEDs. "
        "The JSON should have a structure where 'ledStrip' is an object containing 'totalLEDs' and 'sequence'. "
        "'totalLEDs' is the number of LEDs, which is always 30, and 'sequence' is an array of frames. "
        "Each frame has 'frameDuration' in milliseconds and 'ledStates', an array representing the state of each LED. "
        "Each 'ledState' has 'index', 'color' (as an RGB array), and 'brightness' (0-255). "
        "Based on this description, create a JSON sequence for: " + description
    )

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "system", "content": json_format_description}]
        # response_format=[{"type": "json_object"}]
    )

    sequence = response.choices[0].message.content  # Corrected attribute access

    try:
        json_sequence = json.loads(sequence)
        return json_sequence
    except json.JSONDecodeError:
        return "Error in JSON format"

# Example usage
description = "a sequence where the first half of the LEDs gradually turn from red to blue and the second half blinks green"
json_sequence = create_led_sequence(description)

print(json.dumps(json_sequence, indent=4))
