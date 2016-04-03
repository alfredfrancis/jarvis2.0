import RPi.GPIO as GPIO
import smbus
import pigpio
import DHT22
from time import sleep
import urllib2
import threading
import datetime
import json
import serial
import thread

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
global m2
global presence
presence = 0
m2=GPIO.input(motion_pin)
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

def update_presence():
	global presence
	while True:
		with serial.Serial('/dev/ttyUSB0') as ser:
			line = ser.readline()
			if "1" in line:
				presence = 1
			else:
				presence = 0
thread.start_new_thread( update_presence, ( ) )

def MOTION(PIR_PIN):
	print "Event triggered : motion"
	global m2
	m2 = 1


def check_presence():
  print("checking motion")
  global m2
  m2 = 0
  threading.Timer(300.0, check_presence).start()
  

threading.Timer(300.0, check_presence).start()

GPIO.add_event_detect(motion_pin, GPIO.RISING, callback=MOTION)


##################################### Motion detection end

def update_db():
  humidity, temperature = readDHT22()
  light = readLight()
  global presence
  r_time = str(datetime.datetime.now().hour)+"."+str(datetime.datetime.now().minute)
  print("-----------------")
  print "presence:" + str(presence)
  print "Light:" + light
  print("Humidity: " + humidity + "%")
  print("Temperature: " + temperature + "C")
  print("time: " + r_time)
  print("motion: " + str(m2))
  print("-----------------")
  try: 
  	urllib2.urlopen("http://10.42.0.1:5000/req_rasp?l="
  		+str(light)+"&t="+str(temperature)+"&h="+str(humidity)+"&m="+str(presence)+"&c="+str(r_time)+"&m2="+str(m2))
  except :
		"error" 
  threading.Timer(5.0, update_db).start()

update_db()

def update_devices():
  response = urllib2.urlopen("http://10.42.0.1:5000/instance")
  status = response.read()
  devices = json.loads(status)
  GPIO.output(23, not bool(int(devices['b1'])))
  GPIO.output(24, not bool(int(devices['b2'])))
  GPIO.output(25, not bool(int(devices['f1'])))
  threading.Timer(2.0, update_devices).start()

update_devices()

def insert_db():
  print("inserting")
  try: 
    urllib2.urlopen("http://10.42.0.1:5000/insert")
  except :
    "error" 
  threading.Timer(300.0, update_db).start()
threading.Timer(300.0, update_db).start() 
def bg_prediction():
  print("inserting")
  try: 
    urllib2.urlopen("http://10.42.0.1:5000/predict")
  except :
    "error" 
  threading.Timer(4.0, bg_prediction).start()  
bg_prediction()

while 1:
  sleep(sleepTime)

