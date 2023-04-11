import math
from board import SCL,SDA
import busio
from adafruit_pca9685 import PCA9685
import time

import datetime
from datetime import timezone 
import time

#Reading of 0 means magnet detected,
#reading of 1 means no magnet detected

import RPi.GPIO as IO
import time
import sys
import argparse
import busio
import smbus
from time import sleep
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
import math


def Servo_Motor_Initialization():
   i2c_bus = busio.I2C(SCL,SDA)
   pca = PCA9685(i2c_bus)
   pca.frequency = 100
   return pca

def Motor_Start(pca):
   x = input("Press and hold ez button. When RED LED turns red wait 3 seconds.")
   Motor_Speed(pca, 1.0)


def Motor_Speed(pca,percent):
   #converts a -1 to 1 value to 16-bit duty cycle
   speed = ((percent) * 3276) + 65535 * 0.15
   pca.channels[15].duty_cycle = math.floor(speed)
   print(speed/65535)

#initialization
pca = Servo_Motor_Initialization()
Motor_Start(pca)



t = time.time()
print(t)

tnew = time.time()
print(tnew)

tdelta = t-tnew
print(tdelta)

IO.setwarnings(False)
IO.setmode(IO.BCM)

GPIO_num = 16
IO.setup(GPIO_num,IO.IN,IO.PUD_UP)
print("program running")

#Get Start Time
start = time.time()
lastTime = start
#Get Time between data data check
samplePeriod = 0.001

curPinValue = 1
lastPinValue = 0

counter = 0

while True:
	
	#update current time
	curTime = time.time()
	
	#if the difference between current time and start time is more than the sample period...
	if curTime - lastTime >=  samplePeriod:
		
		#take the data from GPIO magnet pin
		curPinValue = IO.input(GPIO_num)
		#print("current reading : ")
		
		#print("current Pin Value = ", curPinValue)
		
		
		#if the magnet is detected and the last reading was not detected last reading
		if curPinValue == 0 and curPinValue != lastPinValue:
			#Take the counter value
			counterTotal = counter
			
			#RPS calculation
			revolutionTime = counterTotal*samplePeriod
			print(revolutionTime)
			RPScalc = 1/revolutionTime
			
			print('RPS calculation = ', RPScalc)
			
			#Reset Count to 0
			counter = 0
		else:
			counter += 1
			#print(counter)
			
		lastPinValue = curPinValue
		lastTime = time.time()


#Footer