#!/usr/bin/python
import RPi.GPIO as GPIO
import spidev
import time
import os
from time import sleep, strftime, time

# Open SPI bus
spi = spidev.SpiDev()
spi.open(0,0)

#Relay = 21
#Relay2 = 20

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
#GPIO.setup(Relay, GPIO.OUT)
#GPIO.setup(Relay2, GPIO.OUT)
#GPIO.output(Relay, GPIO.HIGH)
#GPIO.output(Relay2, GPIO.HIGH)

# Function to read SPI data from MCP3008 chip
# Channel must be an integer 0-7
def ReadChannel(channel):
  spi.max_speed_hz = 1350000
  adc = spi.xfer2([1,(8+channel)<<4,0])
  print( "raw data", adc)
  data = ((adc[1]&3) << 8) + adc[2]
  return data

# Function to convert data to voltage level,
# rounded to specified number of decimal places.
def ConvertVolts(data,places):
  volts = (data * 5.08 ) / float(1023)
  volts = round(volts,places)
  return volts
def write_volts(volts):
    with open("charge_volts.csv", "a") as log:
            log.write("{0},{1},{2}\n".format(strftime("%Y-%m-%d %H:%M:%S"),c_volts,s_volts))
#        log.write("{0},{1},{2}\n".format(strftime("%Y-%m-%d %H:%M:%S"),i,str(dist)))
#        log.write("{0},{1}\n".format(dutyCycle,str(dist)))


# Define sensor channels
c_channel = 0    # Charging Channel
s_channel = 1    # Solar Channel
# Define delay between readings
delay = 1

while True:

  # Read the gas sensors' data
  c_level = ReadChannel(c_channel)
  c_volts = ConvertVolts(c_level,2)
  s_level = ReadChannel(s_channel)
  s_volts = ConvertVolts(s_level,2)

  write_volts(c_volts)
  # Print out results
  print "--------------------------------------------"
  print("Charging Volts: {} ({}V)".format(c_level,c_volts))
  print("SolarPan Volts: {} ({}V)".format(s_level,s_volts))

  # Wait before repeating loop
  sleep(delay)

