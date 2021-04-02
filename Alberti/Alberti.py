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


def encryptChar(cypher:albertiCypher, message:str, key:int) -> str: 
	posMess = cypher.stationnary.find(message)
	posCypher = (posMess + key) % cypher.modulo
	return cypher.movable[posCypher]

#def encode(cypher:albertiCypher, message) -> str: 
	#return romanNumeral(message)

def encrypt(cypher:albertiCypher, message:str, key:str) -> str:
	message = message.upper()
	#message = encode(cypher, message)
	cryptogram = ""
	posKey = cypher.stationnary.find(key)
	for c in message:
		cryptogram += encryptChar(cypher,c, posKey)
	return cryptogram

s = input()
cryptogram = encrypt(albertiCypher, s, "D")
print(cryptogram)
