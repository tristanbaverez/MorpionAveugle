from grid import *
import socket
import select
import sys

hote = "localhost" #par défault au cas où l'on décide travailler en local
port = 12800 #port d'initialisation

def connexion():
  connexion_avec_serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  connexion_avec_serveur.connect((hote, port))
  print("Connexion établie avec le serveur sur le port {}".format(port))

  
def initialisationClient():
  print('###Mise en réseau - Client')
  try:
    h = input("Tapez l'ip du serveur svp :\n")
    p = int (input("Entrez le numéro de port à présent: \n"))
  except TypeError:
    print("Type incompatible")
  except NameError:
    print("### ERREUR -> Saisie invalide, veuillez relancer une demande de serveur")
  else:
    hote=h
    port=p
    
initialisationClient();  

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
