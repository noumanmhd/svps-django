import RPi.GPIO as GPIO
import time
GPIO.setwarnings(False)

class Barrier:
    def __init__(self, servo_pin=26):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(servo_pin, GPIO.OUT)
        self.p = GPIO.PWM(servo_pin, 50) # GPIO 17 for PWM with 50Hz
        self.p.start(6) # Initialization
        self.bclose()
        
    def bopen(self):
        self.p.ChangeDutyCycle(2.5)
        time.sleep(3)
        
    def bclose(self):
        self.p.ChangeDutyCycle(8)
        print("CLOSE")
        time.sleep(1)
        
    def bstop(self):
        self.p.stop()
        GPIO.cleanup()
