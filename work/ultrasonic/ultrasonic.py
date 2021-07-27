import RPi.GPIO as GPIO
import time
 

class Ultrasonic:
    def __init__(self, echo=24, trigger=18, limit=2.5):
        GPIO.setwarnings(False)
        #GPIO Mode (BOARD / BCM)
        GPIO.setmode(GPIO.BCM)
        self.echo = echo
        self.trigger = trigger
        self.limit = limit
    
        #set GPIO direction (IN / OUT)
        GPIO.setup(self.trigger, GPIO.OUT)
        GPIO.setup(self.echo, GPIO.IN)
 
    
    def distance(self):
        # set Trigger to HIGH
        GPIO.output(self.trigger, True)
    
        # set Trigger after 0.01ms to LOW
        time.sleep(0.00001)
        GPIO.output(self.trigger, False)
    
        StartTime = time.time()
        StopTime = time.time()
    
        # save StartTime
        while GPIO.input(self.echo) == 0:
            StartTime = time.time()
    
        # save time of arrival
        while GPIO.input(self.echo) == 1:
            StopTime = time.time()
    
        # time difference between start and arrival
        TimeElapsed = StopTime - StartTime
        # multiply with the sonic speed (34300 cm/s)
        # and divide by 2, because there and back
        distance = (TimeElapsed * 34300) / 2
    
        return distance
    
    def detected(self):
        distance = self.distance()
        if distance <= self.limit:
            return True
        return False

 
