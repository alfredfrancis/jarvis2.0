import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.IN)

fo = open("log.csv", "a+")
fo.write( "second,flag\n")
count = 0
counter = 0
flag = 0
while True:
  i=GPIO.input(7)
  if i==1:
    flag += 1
    print "Motion in" + str(count)
  time.sleep(1)
  count += 1
  if count == 60 :
  	count =0
  	print "Motion in" + str(counter) + " minute : " + str(flag)
  	fo.write( str(counter) +","+ str(flag) +"\n")
  	flag = 0
  	counter +=1



