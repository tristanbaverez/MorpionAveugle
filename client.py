from grid import *
import socket
import select
import sys

hote = "" #vide par défault
port = 12800 
launchOK=False
def connexion():
  connexion_avec_serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  connexion_avec_serveur.connect((hote, port))
  print("Connexion établie avec le serveur sur le port {}".format(port))
  return True
  
def initialisationClient():
  print('###Mise en réseau - Client')
  try:
    if len(sys.argv) != 2:
      print("Erreur : nombre d'arguments invalide")
    else:
      h=sys.gethostbyname(sy.argv[1])
      p = int (input("Entrez le numéro de port svp (voir port serveur): \n"))
  except TypeError:
    print("Type incompatible")
  except NameError:
    print("### ERREUR -> Saisie invalide, veuillez relancer une demande de serveur")
  else:
    #on suppose que le hostname est entré correctement
    port=p
    launchOK=connexion()
    
initialisationClient();  

def intercation():
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

if launchOK:
  intercation()