import RPi.GPIO as GPIO
import smbus
import pigpio
import DHT22
from time import sleep
import urllib2
import threading
import datetime
import json
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

# We want our sleep time to be above 3 seconds.
sleepTime = 3

GPIO.setmode(GPIO.BCM) 
GPIO.setup(relay_pin1,GPIO.OUT)
GPIO.setup(relay_pin2,GPIO.OUT)
GPIO.setup(relay_pin3,GPIO.OUT)
GPIO.setup(motion_pin, GPIO.IN)

presence = GPIO.input(motion_pin)

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

##################################### Motion detection 

def MOTION(PIR_PIN):
	print "Event triggered : motion"
	print "Performing Prediction"
	global presence
	presence = 1
	try: 
		response = urllib2.urlopen("http://10.42.0.1:5000/predict")
	except:
		print "error"
	print "Prediction complete"

def check_presence():
  print("checking presence")
  global presence
  threading.Timer(300, check_presence).start()
  presence = 0

threading.Timer(300, check_presence).start()

GPIO.add_event_detect(motion_pin, GPIO.RISING, callback=MOTION)

##################################### Motion detection end

def update_db():
  humidity, temperature = readDHT22()
  light = readLight()
  global presence
  r_time = str(datetime.datetime.now().hour)+"."+str(datetime.datetime.now().minute)
  print("-----------------")
  print "Acitivity:" + str(presence)
  print "Light:" + light
  print("Humidity: " + humidity + "%")
  print("Temperature: " + temperature + "C")
  print("time: " + r_time)
  print("-----------------")
  try: 
  	urllib2.urlopen("http://10.42.0.1:5000/req_rasp?l="
  		+str(light)+"&t="+str(temperature)+"&h="+str(humidity)+"&m="+str(presence)+"&c="+str(r_time))
  except :
		"error" 
  threading.Timer(5.0, update_db).start()

update_db()

def insert_db():
  print("inserting")
  try: 
    urllib2.urlopen("http://10.42.0.1:5000/insert")
  except :
    "error" 
  threading.Timer(300.0, update_db).start()

insert_db()

while 1:
  sleep(sleepTime)

