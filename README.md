# Alberti

À quoi sert AlberPi?

AlberPi sert à accélérer le chiffrement et déchiffrement selon le chiffre d’Alberti. 

Pour un cryptogramme donné, il le déchiffre en effectuant les substitutions selon la position du disque mobile.

Pour un message et une clé donnée, il bâtit un cryptogramme selon le chiffre d’Alberti.

Démarrage rapide

Pour démarrer le programme
pi@raspberrypi:~$ python3 disqueAlberti.py
Ceci démarre le programme avec un cryptogramme par défaut.

Pour démarrer le programme avec un cryptogramme donné
pi@raspberrypi:~$ python3 disqueAlberti.py QbinxmFbxudssigyyutscooNc
Les caractères qui n’apparaissent pas sur le disque mobile sont ignorés

Pour chiffrer un message et obtenir un cryptogramme
pi@raspberrypi:~$ python3 chiffreAlberti.py "La carotte est cuite." x
Si la clé n’est pas donnée ou est invalide, la clé par défaut est k.

Quand la LED est à son plus fort, centrer le g sur le A.
 
