import RPi.GPIO as GPIO
import time
import sys

# Servo control settings
OFFSET_DUTY = 0.5        
SERVO_MIN_DUTY = 2.5 + OFFSET_DUTY     
SERVO_MAX_DUTY = 12.5 + OFFSET_DUTY    
SERVO_DELAY_SEC = 0.2  # Adjust this for smoother movements
servoPin = 12

def setup():
    global p
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(servoPin, GPIO.OUT)
    GPIO.output(servoPin, GPIO.LOW)

    p = GPIO.PWM(servoPin, 50)
    p.start(0)
    
def servoWrite(angle):
    if angle < 0:
        angle = 0
    elif angle > 180:
        angle = 180
    dc = SERVO_MIN_DUTY + (SERVO_MAX_DUTY - SERVO_MIN_DUTY) * angle / 180.0
    p.ChangeDutyCycle(dc)
    
def text_to_movement(text):
    for char in text:
        if char.lower() in 'aeiou':  # Vowel - mouth more open
            servoWrite(45)
        else:  # Consonant or other - mouth closed
            servoWrite(100)
        time.sleep(SERVO_DELAY_SEC)

    # Ensure the mouth ends up closed
    servoWrite(160)

def destroy():
    servoWrite(160)
    p.stop()
    GPIO.cleanup()

if __name__ == '__main__':
    setup()
    try:
        input_text = sys.argv[1] if len(sys.argv) > 1 else "Det tog chatGPT et minut at opdatere motormouth.py så den tager en tekst som input og åbner munden mere ved vokaler end ved konsonanter"
        text_to_movement(input_text)
    except KeyboardInterrupt:
        destroy()
