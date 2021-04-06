import math
import random

class Param :
	subMessageLength = 10
	subMessageMinLength = 1
	probaDigit = 5

class Disk:
	stationnary = "ABCDEFGILMNOPQRSTVXZ1234"
	movable =     "gklnprtuz&xysomqihfdbace"
	size = len(stationnary)
	nbKeys = len(stationnary) - 4
	regexCryptogram = "ABCDEFGILMNOPQRSTVXZgklnprtuz&xysomqihfdbace"
        
encoding = {
	"H" : "FF",
	"J" : "II",
	"K" : "QQ",
	"U" : "VV",
	"W" : "XX",
	"Y" : "ZZ"
}

def lengthCrypto():
	return Param.subMessageLength * math.exp(-1 * random.random() * Param.subMessageLength) + Param.subMessageMinLength


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
	indexMessage:int = 0;
	print("Key = " + str(Disk.movable.find(key)) + "(" + key + ")")
	while indexMessage < len(message):
		indLettre = nextLettre()
		cryptogram += Disk.stationnary[indLettre]
		posKey = (posKeyRotary - indLettre) % Disk.size
		
		print (Disk.stationnary[indLettre])
		printDisk(posKey)

		next = min(indexMessage + lengthCrypto(), len(message))
		while indexMessage < next :
			cryptogram += encryptChar(message[indexMessage], posKey)
			indexMessage += 1;
			
	return cryptogram


def decryptChar(message:str, key:int) -> str: 
	posMess = Disk.movable.find(message)
	posCypher = (posMess - key) % Disk.size
	return Disk.stationnary[posCypher]


def decrypt(cryptogram:str, position:int) :
	message = ""
	for c in cryptogram :
		message += decryptChar(c, position)
	return message



#todo man page
#todo cleanup message
#todo argument message et clé

def run():
        s = input()
        cryptogram = encrypt(s, "e")
        print(cryptogram)
        print()

