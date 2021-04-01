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



romanNumerals : List[Tuple[int, str]] = [(1000, "M"), (500, "D"), (100, "C"), (50 ,"L"), (10, "X"), (5, "V"), (1, "I")]

def romanNumeral(n:int) -> str:
	roman = ""
	for ind in romanNumerals :
		print (ind)
		while n > ind[0]:
			roman += ind[1]
			n -= ind[0]
		
	return roman


def encryptChar(cypher:albertiCypher, message:str, key:int) -> str: 
	posMess = cypher.stationnary.find(message)
	posCypher = (posMess + key) % cypher.modulo
	return cypher.movable[posCypher]

def encode(cypher:albertiCypher, message) -> str: 
	return romanNumeral(message)

def encrypt(cypher:albertiCypher, message:str, key:str) -> str: 
	message = message.capitalize
	message = encode(cypher, message)
	cryptogram = ""
	posKey = cypher.stationnary.find(key)
	for c in message:
		cryptogram += encryptChar(cypher,c, posKey)
	return cryptogram

cryptogram = encrypt(albertiCypher,"45","D")
print(cryptogram)
