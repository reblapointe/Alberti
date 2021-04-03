from typing import List
from typing import Tuple
import math
import random

class Disk:
	stationnary = "ABCDEFGILMNOPQRSTVXZ1234"
	movable =     "gklnprtuz&xysomqihfdbace"
	size = len(stationnary)
	nbKeys = len(stationnary) - 4

encoding = {
	"H" : "FF",
	"J" : "II",
	"K" : "QQ",
	"U" : "VV",
	"W" : "XX",
	"Y" : "ZZ"
}

def lengthCrypto():
	averageLength:float = 5

	return averageLength * math.exp(-1 * random.random() * averageLength)


def nextLettre():
	return random.randint(0, Disk.nbKeys - 1)


def encryptChar(message:str, key:int) -> str: 
	posMess = Disk.stationnary.find(message)
	posCypher = (posMess + key) % Disk.size
	return Disk.movable[posCypher]

def encode(message) -> str: 
	for e in encoding:
		message = message.replace(e, encoding[e])
	return message

def printDisk(posKey): 
	print("État du disque : ")
	for c in Disk.stationnary:
		print(c, end = '')
	s = 0
	print()
	while s < Disk.size :
		print(Disk.movable[posKey], end = '')
		s += 1
		posKey = (posKey + 1) % Disk.size
	print()

def encrypt(message:str, key:str) -> str:
	message = message.upper()
	message = encode(message)
	posKeyRotary:int = Disk.movable.find(key)
	cryptogram = ""
	indice:int = 0;
	print("Key = " + key, end = '')
	print ("(" + str(Disk.movable.find(key)) + ")")
	while indice < len(message):
		indLettre = nextLettre()
		print ("IndLettre = " + str(indLettre), end = '')
		cryptogram += Disk.stationnary[indLettre]
		print ("(" + Disk.stationnary[indLettre] + ")")
		posKey = (posKeyRotary - indLettre) % Disk.size

		printDisk(posKey)
		next = min(indice + lengthCrypto(), len(message))
		while indice < next :
			cryptogram += encryptChar(message[indice], posKey)
			indice = indice + 1;
			
	return cryptogram

s = input()
cryptogram = encrypt(s, "k")
print(cryptogram)
