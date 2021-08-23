#!/usr/bin/python3
# coding=utf-8

# to change message :
# mosquitto_pub -h mqtt -t alberti/msg -m 'kLes carottes sont cuites' -r
# first letter is the key

import chiffreAlberti as alberti
import os, sys, re, time, datetime, subprocess, paho.mqtt.client as paho
import smbus, I2C_LCD_driver, RPi.GPIO as GPIO, deviceAddresses
# source code : https://embeddedcircuits.com/raspberry-pi/tutorial/raspberry-pi-potentiometer-tutorial

# Potentiometer
address = deviceAddresses.POT_ADDRESS
bus = smbus.SMBus(1) #initialize System Management Bus to enable I2C communication
cmd = 0x40  # control byte to enable analog output

letterVoltage = [238, 225, 217, 206, 198, 188, 179, 168, 158, 149, 140, 127, 119, 109, 99, 89, 79, 68, 60, 50, 39, 31, 19, 11]
#cryptogram
cryptogram = "QbinxmFbxvdssigyyvtscooNcvdty"
pos = 0
run = True
refresh = False

# LCD
mylcd = I2C_LCD_driver.lcd()

# MQTT
mqttBroker = deviceAddresses.MQTT_BROKER
mqttPort = deviceAddresses.MQTT_PORT
mqttMessageTopic = deviceAddresses.MQTT_MESSAGE_TOPIC
mqttCryptoTopic = deviceAddresses.MQTT_CRYPTO_TOPIC
mqttClient = 0

# GPIO Buttons
leftButton = deviceAddresses.LEFT_BUTTON_GPIO
rightButton = deviceAddresses.RIGHT_BUTTON_GPIO
shutdownButton = deviceAddresses.SHUTDOWN_BUTTON_GPIO

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
                          bouncetime = 2000)

def onMessage(client, userdata, message):
    global cryptogram
    global refresh
    global pos
    payload = str(message.payload.decode('utf-8'))
    if message.topic == mqttMessageTopic :
        key = payload[0]
        message = alberti.encode(payload[1:])
        cryptogram = alberti.encrypt(key = key, message = message)
    else :
        cryptogram = alberti.cleanupCryptogram(payload)
    refresh = True
    pos = 0

def initMQTT() :
    global mqttClient
    mqttClient = paho.Client()
    mqttClient.on_message = onMessage
    mqttClient.connect(mqttBroker, mqttPort)
    mqttClient.loop_start()
    mqttClient.subscribe([(mqttMessageTopic, 0), (mqttCryptoTopic, 0)])

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
    c = c.ljust(16, " ")
    t = t.ljust(16, " ")
    print(c[pos : pos + 16])
    print(t[pos : pos + 16])
    mylcd.lcd_display_string(c[pos:], 1)
    mylcd.lcd_display_string(t[pos:], 2)

def leftButtonCallback(channel) :
    global pos
    global refresh
    refresh = True
    pos = 0 if pos == 0 else pos - 1

def rightButtonCallback(channel) :
    global pos
    global refresh
    if (len(cryptogram) > 16) :
        refresh = True
        pos = min(pos + 1, abs(len(cryptogram) - 16))

def loop():
    key = 0
    global refresh
    while True :
        value = analogRead(0)
        analogWrite(value)
        i = 0
        newKey = 0
#        if nvalue != value:
#            print(nvalue)
        while i < len(letterVoltage) and letterVoltage[i] > value :
            i = i + 1
            newKey = i

        if i == len(letterVoltage) :
            newKey = 0

        #newKey = int((244 - value) / 244 * alberti.Disk.size - 1)
        if (key != newKey or refresh) and run:
            os.system('clear')
            refresh = False
            key = newKey
            print(value)
            print(key)
            alberti.printDisk(key)
            print()
            print(cryptogram)
            print(alberti.decrypt(cryptogram, key))

            print()
            imprimer(cryptogram, alberti.decrypt(cryptogram, key))
            print()
        time.sleep(0.001)

def get_ip():
    cmd = "hostname -I | cut -d\' \' -f1"
    return subprocess.check_output(cmd, shell=True).decode("utf-8").strip()

def shutdown(channel):
    global run
    if run :
        run = False
        try :
            mqttClient.loop_stop()
            imprimer('Fermeture', 'Debrancher apres')
            time.sleep(2)
            imprimer('Debrancher apres', '30 secondes')
            time.sleep(2)
            mylcd.lcd_clear()
            mylcd.backlight(0)
        except Exception as e :
            print(str(e))
        os.system("sudo shutdown -h now")

def printConfiguration() :
    imprimer('Demarrage', '')
    time.sleep(1)
    imprimer(datetime.datetime.now().strftime('%d %b %H:%M:%S'), get_ip())
    time.sleep(3)
    imprimer('MQTT BROKER ' + str(mqttPort), mqttBroker)
    time.sleep(2)
    imprimer('Message Topic', mqttMessageTopic)
    time.sleep(2)
    imprimer('Crypto Topic', mqttCryptoTopic)
    time.sleep(2)

def setup() :
    try :
        initMQTT()
        imprimer('Connexion MQTT', 'reussie')
    except Exception as e :
        print(e)
        imprimer('Connexion MQTT', 'echouee')
    time.sleep(2)

    buttonsSetup()

# Start
printConfiguration()
setup()
if len(sys.argv) > 1 :
    cryptogram = alberti.cleanupCryptogram(sys.argv[1])

if __name__ == '__main__':
    try:
        loop()
    except KeyboardInterrupt: # press Ctrl + C to exit script
        destroy()
