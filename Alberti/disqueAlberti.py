#!/usr/bin/python3
import smbus
import time
import algoAlberti as alberti
import os
import sys
import re

# source code : https://embeddedcircuits.com/raspberry-pi/tutorial/raspberry-pi-potentiometer-tutorial

address = 0x48
bus = smbus.SMBus(1)    #initialize System Management Bus to enable I2C communication
cmd = 0x40  # control byte to enable analog output 
cryptogram = "OcfBqlNqrByiiBpqqyxilhhuipq"

if len(sys.argv) > 1 :
    cryptogram = sys.argv[1]
cryptogram = re.sub("[^" + alberti.Disk.regexCryptogram + "]", "", cryptogram)

print("Cryptogramme : " + cryptogram)
# read the digital quantity representation of an analog signal from one of the pins of the AD Converter
# chn (Channels) ranges from 0 to 3 to read analog input from  A0, A1, A2 & A3 pins
def analogRead(chn):
    value = bus.read_byte_data(address, cmd+chn) # cmd is not necessary but is added to make sure the correct control byte is defined
    return value
     
# write to DAC and output analog signal from ADC's AOUT pin
def analogWrite(value):
    bus.write_byte_data(address, cmd, value)
     
def loop():
    while True:
        os.system('clear')
        value = analogRead(0)
        analogWrite(value)
        print(value)
        key = int((256 - value) / 255 * alberti.Disk.size - 1)
        alberti.printDisk(key)
        print(cryptogram)
        print(alberti.decrypt(cryptogram, key))
        time.sleep(0.1)
         
def destroy():
    bus.close()
     
if __name__ == '__main__':
    try:
        loop()
    except KeyboardInterrupt: # press Ctrl + C to exit script
        destroy()
