#!/usr/bin/python3
import chiffreAlberti as alberti
import os, sys, re, time, datetime, subprocess
import smbus, I2C_LCD_driver, RPi.GPIO as GPIO
# source code : https://embeddedcircuits.com/raspberry-pi/tutorial/raspberry-pi-potentiometer-tutorial

# Potentiometer
address = 0x48
bus = smbus.SMBus(1) #initialize System Management Bus to enable I2C communication
cmd = 0x40  # control byte to enable analog output

#cryptogram
cryptogram = "QbinxmFbxudssigyyutscooNcudty"
pos = 0

# LCD
mylcd = I2C_LCD_driver.lcd()

# MQTT
mqttBroker = '192.168.1.100'
mqttPort = 1883
mqttCryptogramTopic = 'alberti/crypto'
mqttClient = 0

# GPIO Buttons
leftButton = 10
rightButton = 11
timePressed = 0

def buttonsSetup():
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(leftButton, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
    GPIO.add_event_detect(leftButton,
                          GPIO.RISING,
                          callback = leftButtonCallback,
                          bouncetime = 200)

    GPIO.setup(rightButton, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
    GPIO.add_event_detect(rightButton,
                          GPIO.RISING,
                          callback = rightButtonCallback,
                          bouncetime = 200)

def onPublish(client, userdata, result):
    cryptogram = alberti.cleanupCryptogram(userdata)

def initMQTT() :
    global mqttClient
    client = paho.Client()
    client.on_publish = onPublish
    client.connect(mqttBroker, mqttPort, 3600)

def analogRead(chn):
    value = bus.read_byte_data(address, cmd + chn)
    # cmd is not necessary but is added to make sure the correct control byte is defined
    return value

# write to DAC and output analog signal from ADC's AOUT pin
def analogWrite(value):
    bus.write_byte_data(address, cmd, value)

def destroy():
    bus.close()
    mqttClient.disconnect()

def imprimer(c, t) :
        global pos
        c = c.ljust(16, ' ')
        t = t.ljust(16, ' ')
	# si on depasse ca repete la derniere lettre
        pos = min(pos, abs(len(c) - 16))
        mylcd.lcd_display_string(c[pos:], 1)
        mylcd.lcd_display_string(t[pos:], 2)

def leftButtonCallback(channel) :
      global pos
      pos = (pos - 1) % 16

def rightButtonCallback(channel) :
      global pos
      pos = (pos + 1) % 16

def downCallback(channel) :
     global timePressed
     timePressed = time.time()

def loop():
    while True:
        os.system('clear')
        value = analogRead(0)
        analogWrite(value)
        key = int((256 - value) / 255 * alberti.Disk.size - 1)
        alberti.printDisk(key)
        print(cryptogram)
        print(alberti.decrypt(cryptogram, key))
        imprimer(cryptogram, alberti.decrypt(cryptogram,key) )
        time.sleep(0.01)

def get_ip():
    cmd = "hostname -I | cut -d\' \' -f1"
    return subprocess.check_output(cmd, shell=True).decode("utf-8").strip()

def shutdown(channel):
    imprimer('Shutting Down', '')
    time.sleep(5)
    os.system("sudo shutdown -h now")

 
### START ###
pos = 0
imprimer('Demarrage', '')
time.sleep(1)
imprimer('MQTT BROKER ' + str(mqttPort), mqttBroker)
time.sleep(2)
imprimer('MQTT Topic', mqttCryptogramTopic)
time.sleep(1)

try :
	initMQTT()
	imprimer('Connexion MQTT', 'reussie')
except Exception :
	imprimer('Connexion MQTT', 'echouee')
time.sleep(1)

imprimer(datetime.datetime.now().strftime('%d %b %H:%M:%S'),
	get_ip())

time.sleep(5)

buttonsSetup()
if len(sys.argv) > 1 :
    cryptogram = alberti.cleanupCryptogram(sys.argv[1])

if __name__ == '__main__':
    try:
        loop()
    except KeyboardInterrupt: # press Ctrl + C to exit script
        destroy()
