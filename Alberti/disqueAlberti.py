#!/usr/bin/python3
# coding=utf-8
import chiffreAlberti as alberti
import os, sys, re, time, datetime, subprocess, paho.mqtt.client as paho
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
mqttTopic = 'alberti'
mqttClient = 0

# GPIO Buttons
leftButton = 10
rightButton = 11
shutdownButton = 4

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

    GPIO.setup(shutdownButton, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
    GPIO.add_event_detect(shutdownButton, GPIO.RISING,
                          callback = shutdown,
                          bouncetime = 200)

def onMessage(client, userdata, message):
    global cryptogram
    global refresh
    payload = str(message.payload.decode('utf-8'))
    key = payload[0]
    message = alberti.encode(payload[1:])
    cryptogram = alberti.encrypt(key = key, message = message)
    refresh = True

def initMQTT() :
    global mqttClient
    mqttClient = paho.Client()
    mqttClient.on_message = onMessage
    mqttClient.connect(mqttBroker, mqttPort)
    mqttClient.loop_start()
    mqttClient.subscribe(mqttTopic)

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
    print(c[pos : pos + 16])
    print(t[pos : pos + 16])
    mylcd.lcd_display_string(c[pos:], 1)
    mylcd.lcd_display_string(t[pos:], 2)

refresh = False
def leftButtonCallback(channel) :
    global pos
    global refresh
    refresh = True
    pos = 0 if pos == 0 else pos - 1

def rightButtonCallback(channel) :
    global pos
    global refresh
    refresh = True
    pos = min(pos + 1, abs(len(cryptogram) - 16))

def loop():
    key = 0
    global refresh
    while True :
        value = analogRead(0)
        analogWrite(value)
        newKey = int((256 - value) / 255 * alberti.Disk.size - 1)
        if key != newKey or refresh :
            os.system('clear')
            refresh = False
            alberti.printDisk(key)

            print()
            print(cryptogram)
            print(alberti.decrypt(cryptogram, key))

            print()
            imprimer(cryptogram, alberti.decrypt(cryptogram,key))
        key = newKey
        time.sleep(0.01)

def get_ip():
    cmd = "hostname -I | cut -d\' \' -f1"
    return subprocess.check_output(cmd, shell=True).decode("utf-8").strip()

def shutdown(channel):
    imprimer('Shutting Down', '')
    client.loop_stop()
    time.sleep(1)
    mylcd.backlight(0)
    os.system("sudo shutdown -h now")

### START ###
pos = 0
imprimer('Demarrage', '')
time.sleep(1)
imprimer('MQTT BROKER ' + str(mqttPort), mqttBroker)
time.sleep(2)
imprimer('MQTT Topic', mqttTopic)
time.sleep(1)

try :
    initMQTT()
    imprimer('Connexion MQTT', 'reussie')
except Exception as e :
    print(e)
    imprimer('Connexion MQTT', 'echouee')

time.sleep(1)

imprimer(datetime.datetime.now().strftime('%d %b %H:%M:%S'), get_ip())
time.sleep(5)

buttonsSetup()
if len(sys.argv) > 1 :
    cryptogram = alberti.cleanupCryptogram(sys.argv[1])

if __name__ == '__main__':
    try:
        loop()
    except KeyboardInterrupt: # press Ctrl + C to exit script
        destroy()
