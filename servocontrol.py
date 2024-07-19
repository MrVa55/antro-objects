import RPi.GPIO as GPIO
import time

# Servo control settings
OFFSET_DUTY = 0.5        
SERVO_MIN_DUTY = 2.5 + OFFSET_DUTY     
SERVO_MAX_DUTY = 12.5 + OFFSET_DUTY    
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

def get_angle_input():
    while True:
        try:
            angle = float(input("Enter an angle (0-180): "))
            return angle
        except ValueError:
            print("Invalid input. Please enter a number between 0 and 180.")

def move_servo_to_angle():
    try:
        while True:
            angle = get_angle_input()
            servoWrite(angle)
    except KeyboardInterrupt:
        destroy()

def destroy():
    p.stop()
    GPIO.cleanup()

if __name__ == '__main__':
    setup()
    try:
        move_servo_to_angle()
    except KeyboardInterrupt:
        destroy()

