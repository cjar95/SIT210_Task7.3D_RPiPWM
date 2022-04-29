#!/usr/bin/env python
# coding: utf-8

# In[4]:


#Import of necessary libraries
import RPi.GPIO as GPIO
import time
from gpiozero import DistanceSensor, LED, PWMLED
from signal import pause

#Define Sensor variable connected to Trigger and Echo of the ultrasonic sensor
sensor = DistanceSensor(11, 7, max_distance=2, threshold_distance=0.2)

#Define Led variable connected to pin 21
led = PWMLED(21, active_high = False)

#Led sources its data from the sensor 
led.source = sensor
led.blink(on_time=0, off_time=0, fade_in_time=10, fade_out_time=10)

#Stops the printing of distance to the console in real time
pause()

#GPIO Mode 
GPIO.setmode(GPIO.BCM)

#Define GPIO Pins
GPIO_TRIGGER = 7
GPIO_ECHO = 11

#Define GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)

    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)

    StartTime = time.time()
    StopTime = time.time()

    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()

    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()

    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
    
    return distance

if __name__ == '__main__':
    try:
        while True:
            dist = distance()
            print ("Measured Distance = %.1f cm" % dist)
            time.sleep(1)

    # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()


# In[ ]:




