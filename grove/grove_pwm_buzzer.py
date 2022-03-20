# Import required libraries
import sys
import RPi.GPIO as GPIO
import time

# Set trigger PIN according with your cabling
triggerPIN = 12

# Set PIN to output
GPIO.setmode(GPIO.BCM)
GPIO.setup(triggerPIN,GPIO.OUT)

# define PWM signal and start it on trigger PIN
buzzer = GPIO.PWM(triggerPIN, 1000) # Set frequency to 1 Khz
buzzer.start(10) # Set dutycycle to 10

# this row makes buzzer work for 1 second, then
# cleanup will free PINS and exit will terminate code execution
time.sleep(1)

GPIO.cleanup()
sys.exit()

# Please find below some addictional commands to change frequency and
# dutycycle without stopping buzzer, or to stop buzzer:
#
# buzzer.ChangeDutyCycle(10)
# buzzer.ChangeFrequency(1000)
# buzzer.stop()
