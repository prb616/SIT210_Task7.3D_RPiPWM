import RPi.GPIO as GPIO
import time

# Set the mode to use BCM pin numbering
GPIO.setmode(GPIO.BCM)

# Define the GPIO pins for the ultrasonic sensor and the buzzer
TRIG = 3  # GPIO pin for the trigger of the ultrasonic sensor
ECHO = 2  # GPIO pin for the echo of the ultrasonic sensor
BUZZ = 13  # GPIO pin for the buzzer

# Set up the GPIO pins for their respective purposes
GPIO.setup(TRIG, GPIO.OUT)  # TRIG is an output
GPIO.setup(ECHO, GPIO.IN)   # ECHO is an input
GPIO.setup(BUZZ, GPIO.OUT)  # BUZZ is an output

# Turn on the buzzer and create a PWM (Pulse Width Modulation) object
GPIO.output(BUZZ, True)
buzzer = GPIO.PWM(BUZZ, 0.25)
buzzer.start(1)

# Function to measure the distance using the ultrasonic sensor
def getDistance():
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)
    start = time.time()
    stop = time.time()

    while GPIO.input(ECHO) == 0:
        start = time.time()

    while GPIO.input(ECHO) == 1:
        stop = time.time()

    timeDifference = stop - start
    distance = (timeDifference * 34300) / 2  # Calculate the distance in centimeters
    return distance

# Function to determine the buzzer frequency based on the distance
def getFrequency(distance):
    if distance > 500:
        return 0.25
    elif distance > 400:
        return 2
    elif distance > 300:
        return 3
    elif distance > 200:
        return 4
    elif distance > 100:
        return 5
    else:
        return 6

if __name__ == '__main__':
    try:
        while True:
            dist = getDistance()  # Get the distance from the ultrasonic sensor
            freq = getFrequency(dist)  # Determine the frequency based on the distance
            buzzer.ChangeFrequency(freq)  # Set the buzzer frequency
            time.sleep(1)  # Wait for 1 second

    except KeyboardInterrupt:
        GPIO.cleanup()  # Clean up and reset GPIO settings
        buzzer.stop()  # Stop the buzzer PWM
