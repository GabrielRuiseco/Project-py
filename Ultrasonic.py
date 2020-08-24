import RPi.GPIO as GPIO
import time

class Ultrasonic:

    def __init__(self):
        self.TRIG = 23
        self.ECHO = 26
        print("Measuring distance in progress")

    def start(self):
        self.__configure()

    def __configure(self):
        GPIO.cleanup()
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.TRIG, GPIO.OUT)
        GPIO.setup(self.ECHO, GPIO.IN)
        GPIO.output(self.TRIG, False)
        print('Waiting for sensor to settle')
        time.sleep(2)
        GPIO.output(self.TRIG, True)
        time.sleep(0.00001)
        GPIO.output(self.TRIG, False)

    def get_distance(self) -> float:
        while GPIO.input(self.ECHO) == 0:
            pulse_start = time.time()
        while GPIO.input(self.ECHO) == 1:
            pulse_end = time.time()

        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 17150
        distance = round(distance, 2)
        print("Distance:", distance, "cm")
        return distance