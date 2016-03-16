import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD) 
GPIO.setup(11,GPIO.OUT)

while True:
  status = input("Enter status:")
  if status == 1:
  	GPIO.output(11,GPIO.LOW)
	print("Light on")
  elif status == 0:
  	GPIO.output(11,GPIO.HIGH)
	print("Light off")
