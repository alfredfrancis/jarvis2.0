import RPi.GPIO as GPIO
import smbus
import pigpio
import DHT22
from time import sleep
import urllib2

GPIO.setwarnings(False)

DEVICE     = 0x23
POWER_DOWN = 0x00
POWER_ON   = 0x01
RESET      = 0x07

CONTINUOUS_LOW_RES_MODE = 0x13
CONTINUOUS_HIGH_RES_MODE_1 = 0x10
CONTINUOUS_HIGH_RES_MODE_2 = 0x11
ONE_TIME_HIGH_RES_MODE_1 = 0x20
ONE_TIME_HIGH_RES_MODE_2 = 0x21
ONE_TIME_LOW_RES_MODE = 0x23
bus = smbus.SMBus(1)

relay_pin1 = 23
relay_pin2 = 24
relay_pin3 = 25
temp_pin = 22
motion_pin = 18 

# Initiate GPIO for pigpio
pi = pigpio.pi()
# Setup the sensor
dht22 = DHT22.sensor(pi,temp_pin) # use the actual GPIO pin name
dht22.trigger()

# We want our sleep time to be above 2 seconds.
sleepTime = 3

GPIO.setmode(GPIO.BCM) 
GPIO.setup(relay_pin1,GPIO.OUT)
GPIO.setup(relay_pin2,GPIO.OUT)
GPIO.setup(relay_pin3,GPIO.OUT)
GPIO.setup(motion_pin, GPIO.IN)

def readDHT22():
    # Get a new reading
    dht22.trigger()
    # Save our values
    humidity  = '%.2f' % (dht22.humidity())
    temp = '%.2f' % (dht22.temperature())
    return (humidity, temp)

def convertToNumber(data):
  return ((data[1] + (256 * data[0])) / 1.2)

def readLight(addr=DEVICE):
  data = bus.read_i2c_block_data(addr,ONE_TIME_HIGH_RES_MODE_1)
  return str(round((convertToNumber(data)/150)*100)) 


def MOTION(PIR_PIN):
  print "Event Triggered : Motion"

  humidity, temperature = readDHT22()
  print "Light availability:" + readLight()
  print("Humidity is: " + humidity + "%")
  print("Temperature is: " + temperature + "C")

'''
  print "Contacting cloud server for prediction using light = "+readLight() + " & time = 4"

  response = urllib2.urlopen("http://jarvis-cloud.herokuapp.com/predict?motion=1&light=" + readLight() + "&time=4&device=bulb2")
  status = response.read()
  
  print("Predicted Device status :" + status)
  if "1" in status:
  	GPIO.output(11,GPIO.LOW)
  elif "0" in status:
  	GPIO.output(11,GPIO.HIGH)
'''

GPIO.add_event_detect(motion_pin, GPIO.RISING, callback=MOTION)

while 1:
  sleep(sleepTime)





