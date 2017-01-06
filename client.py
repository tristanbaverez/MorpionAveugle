from grid import *
import socket
import select
import sys

hote = "localhost"
port = 12800

connexion_avec_serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connexion_avec_serveur.connect((hote, port))
print("Connexion établie avec le serveur sur le port {}".format(port))

shot = b""

while shot != b"fin":
    signal = connexion_avec_serveur.recv(1024)
    signal = signal.decode()
    print(signal)
    if signal == "yourshot":
        shot = input("> ")
        # Peut planter si vous tapez des caractères spéciaux
        shot = shot.encode()
        # On envoie le message
        connexion_avec_serveur.send(shot)

print("Fermeture de la connexion")
connexion_avec_serveur.close()
