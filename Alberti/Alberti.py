
class albertiCypher:
	stationnary = "ABCDEFGILMNOPQRSTVXZ1234"
	movable =     "gklnprtuz&xysomqihfdbace"
	modulo = len(stationnary)

def encryptChar(cypher:albertiCypher, message:str, key:int): 
	posMess = cypher.stationnary.find(message)
	posCypher = (posMess + key) % cypher.modulo
	return cypher.movable[posCypher]

def encrypt(cypher:albertiCypher, message:str, key:str):
	cryptogram = ""
	posKey = cypher.stationnary.find(key)
	for c in message:
		cryptogram += encryptChar(cypher,c, posKey)
	return cryptogram

def encode(cypher:albertiCypher, message):
	return

cryptogram = encrypt(albertiCypher,"VNEGROSSEFACE","D")
print(cryptogram)
