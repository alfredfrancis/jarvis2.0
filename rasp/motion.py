import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setup(8, GPIO.IN)
while True:
  i=GPIO.input(8)
  if i==1:
    print("Intruder detected",i)
  else:
    print("No Motion",i)
  time.sleep(0.1)
