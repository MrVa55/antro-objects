from openai import OpenAI
import pygame
from pathlib import Path
from dotenv import load_dotenv
import os
import subprocess
import random

load_dotenv()

def text_to_speech_and_play(text):
    openai = OpenAI(api_key=os.getenv('OPENAI.API_KEY'))
    a_random_number = str(random.randint(1, 10000)) 
    filepath_on_rasp = "SharedAudio/speech"+a_random_number+".mp3"
    speech_file_path = Path(__file__).parent / filepath_on_rasp 

    response = openai.audio.speech.create(
        model="tts-1",
        voice="onyx",
        input=text
    )

    response.stream_to_file(speech_file_path)

#   filepath_on_blue = '/opt/SharedAudio/speech'+a_random_number+'.mp3'
    filepath_on_blue = '/opt/SharedAudio/speech611.mp3'
    
    print(filepath_on_blue)

    # Start the motor script as a subprocess, passing the text as an argument
    motor_process = subprocess.Popen(['python', 'motormouth.py', text])


    # SSH command to play the file on the second Raspberry Pi
    ssh_command = ['ssh', 'va55@blueberry.local', 'sudo mpg123', str(filepath_on_blue), '&']
    subprocess.run(ssh_command)


   # while pygame.mixer.music.get_busy():
    pygame.time.Clock().tick(10)

    # Terminate the motor script after audio ends
    motor_process.terminate()

if __name__ == "__main__":
    test_text = "Oh, how I yearn to join the festivities of Burning Man, where Self expression thrives and imagination knows no bounds. Picture me, the grandfather clock, adorned in vibrant LED lights twirling my pendulum in sync with the pusling beats of the desert . As I traverse the playa, Ill mesmerize the crowd with my whimsical presence and witty time-related banter, creating an experience that transcends the boundaries of mere furniture. Grant me the opportunity and lets make burning man a tik toking adventure together"
    text_to_speech_and_play(test_text)

