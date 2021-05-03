#!/usr/bin/python3

import math
import random
import re
import sys

class Param :
	subMessageLength = 10
	probaDigit = 5

class Disk:
	stationnary = "ABCDEFGILMNOPQRSTVXZ1234"
	movable =     "gklnprtuz&xysomqihfdbace"
	size = len(stationnary)
	nbDigits = 4
	nbKeys = len(stationnary) - nbDigits 
	regexMessage = "ABCDEFGILMNOPQRSTVXZ"
	regexCryptogram = "ABCDEFGILMNOPQRSTVXZgklnprtuz&xysomqihfdbace"
	
encoding = {
	"H" : "FF",
	"J" : "II",
	"K" : "QQ",
	"U" : "VV",
	"W" : "XX",
	"Y" : "ZZ"
}

def changeLetter() -> bool:
	return 0 == random.randint(0, Param.subMessageLength)

def nextLettre() -> int :
	return random.randint(0, Disk.nbKeys - 1)

def insertDigit() -> bool:
	return 0 == random.randint(0, Param.probaDigit) 

def encryptChar(message:str, key:int) -> str: 
	posMess = Disk.stationnary.find(message)
	posCypher = (posMess + key) % Disk.size
	return Disk.movable[posCypher]

def encode(message:str) -> str:
	message = message.upper()
	for e in encoding:
		message = message.replace(e, encoding[e])
	message = re.sub("[^" + Disk.regexMessage + "]", "", message)
	encoded = ""
	for m in message :
		encoded += m
		if insertDigit() :
			encoded += str(random.randint(1, Disk.nbDigits))
	return encoded

def encrypt(message:str, key:str) -> str:
	message = encode(message)
	posKeyRotary:int = Disk.movable.find(key)
	cryptogram = ""
	indexMessage:int = 0;
	while indexMessage < len(message):
		indLettre = nextLettre()
		cryptogram += Disk.stationnary[indLettre]
		posKey = (posKeyRotary - indLettre) % Disk.size	
		while indexMessage < len(message) and not changeLetter() :
			cryptogram += encryptChar(message[indexMessage], posKey)
			indexMessage += 1;
	return cryptogram

def decryptChar(message:str, key:int) -> str: 
	posMess = Disk.movable.find(message)
	if (posMess != -1) :
		posCypher = (posMess - key) % Disk.size
		return Disk.stationnary[posCypher]
	else :
		return ""

def decrypt(cryptogram:str, position:int) -> str:
	message = ""
	for c in cryptogram :
		message += decryptChar(c, position)
	return message

def printDisk(posKey:int): 
	for c in Disk.stationnary:
		print(c, end = '')
	s = 0
	print()
	while s < Disk.size :
		print(Disk.movable[posKey], end = '')
		s += 1
		posKey = (posKey + 1) % Disk.size
	print()

def bruteForce(cryptogram:str):
	for i in range(Disk.size):
		printDisk(i)
		print(decrypt(cryptogram, i))
		print()

if __name__ == "__main__":
	message = "Les carottes sont cuites"
	key = "k"
	if len(sys.argv) > 1 :
		message = sys.argv[1]
	if len(sys.argv) > 2 and sys.argv[2][0] in Disk.movable :
		key = sys.argv[2][0]
	print(message)
	print(key)
	message = encode(message)
	print(message)
	cryptogram = encrypt(message, key)
	print(cryptogram)
