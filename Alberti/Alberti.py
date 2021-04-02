from typing import List
from typing import Tuple

class albertiCypher:
	stationnary = "ABCDEFGILMNOPQRSTVXZ1234"
	movable =     "gklnprtuz&xysomqihfdbace"
	modulo = len(stationnary)

encoding = {
	"H" : "FF",
	"J" : "II",
	"K" : "QQ",
	"U" : "VV",
	"W" : "XX",
	"Y" : "ZZ"
}


def encryptChar(message:str, key:int) -> str: 
	posMess = albertiCypher.stationnary.find(message)
	posCypher = (posMess + key) % albertiCypher.modulo
	return albertiCypher.movable[posCypher]

def encode(message) -> str: 
	for e in encoding:
		message = message.replace(e, encoding[e])
	return message
def encrypt(message:str, key:str) -> str:
	message = message.upper()
	message = encode(message)
	cryptogram = ""
	posKey = albertiCypher.stationnary.find(key)
	for c in message:
		cryptogram += encryptChar(c, posKey)
	return cryptogram

s = input()
cryptogram = encrypt(s, "D")
print(cryptogram)
