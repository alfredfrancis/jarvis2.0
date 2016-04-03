import RPi.GPIO as GPIO
from time import sleep
GPIO.setmode(GPIO.BOARD) 
GPIO.setup(23,GPIO.OUT)
GPIO.setup(24,GPIO.OUT)
GPIO.setup(25,GPIO.OUT)
while True:
	GPIO.output(23,GPIO.LOW)
	GPIO.output(23,GPIO.HIGH)
	GPIO.output(24,GPIO.LOW)
	sleep(1)
	GPIO.output(24,GPIO.HIGH)
	GPIO.output(25,GPIO.LOW)	
	sleep(1)
	GPIO.output(25,GPIO.HIGH)
	GPIO.output(23,GPIO.LOW)
