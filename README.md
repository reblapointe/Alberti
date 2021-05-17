# AlberPi

## À quoi sert AlberPi?

AlberPi sert à accélérer le chiffrement et déchiffrement selon le chiffre d’Alberti. 

Pour un cryptogramme donné, il le déchiffre en effectuant les substitutions selon la position du disque mobile.

Pour un message et une clé donnée, il bâtit un cryptogramme selon le chiffre d’Alberti.

## Démarrage rapide

Pour démarrer le programme

`pi@raspberrypi:~$ python3 disqueAlberti.py`  

Pour démarrer le programme avec un cryptogramme donné. Les caractères qui n’apparaissent pas sur le disque mobile sont ignorés  

`pi@raspberrypi:~$ python3 disqueAlberti.py QbinxmFbxudssigyyutscooNc`
 

Pour chiffrer un message et obtenir un cryptogramme. Si la clé n’est pas donnée ou est invalide, la clé par défaut est `k`.   

`pi@raspberrypi:~$ python3 chiffreAlberti.py "Les carottes sont cuites." x` 

Quand la LED est à son plus fort, centrer le *g* sur le *A*.
 
 ## Fabriquer l'appareil
 Voir la [documentation complète](/Alberti/blob/master/documentation/Alberti.docx)
