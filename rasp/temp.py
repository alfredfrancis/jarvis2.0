"""
Remember to start the daemon with the command
'sudo pigpiod' before running this script. It
needs to be restarted every time your pi
is restarted.
"""

import pigpio
import DHT22
from time import sleep

# Initiate GPIO for pigpio
pi = pigpio.pi()
# Setup the sensor
dht22 = DHT22.sensor(pi,22) # use the actual GPIO pin name
dht22.trigger()

# We want our sleep time to be above 2 seconds.
sleepTime = 3

def readDHT22():
    # Get a new reading
    dht22.trigger()
    # Save our values
    humidity  = '%.2f' % (dht22.humidity())
    temp = '%.2f' % (dht22.temperature())
    return (humidity, temp)

while True:
    humidity, temperature = readDHT22()
    print("Humidity is: " + humidity + "%")
    print("Temperature is: " + temperature + "C")
    sleep(sleepTime)


