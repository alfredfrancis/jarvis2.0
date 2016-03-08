import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.IN)
while True:
  i=GPIO.input(7)
  if i==1:
    print("Intruder detected",i)
  else:
    print("No Motion",i)
  time.sleep(0.1)







