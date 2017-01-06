# -*-coding:utf-8 -*
from grid import *
import socket
import select
import sys

hote = "" #vide par défault

def connexion(port, hote):
  connexion_avec_serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  connexion_avec_serveur.connect((hote, port))
  print("Connexion établie avec le serveur sur le port {}".format(port))

  gridsC = [grid(), grid()] # grille du J1 et du J2 pour l'affichage côté client
  shot = ""
  while (shot != "fin") or (signal != b"w1") or (signal != b"w2") or (signal != b"l1") or (signal != b"l2") or (signal != b"draw"):
    signal = connexion_avec_serveur.recv(1024)
    signal = signal.decode()
    print(signal)
    if signal == b"yourshot":
      print("Entrez la coup souhaité")
      shot =input("> ")
      # Peut planter si vous tapez des caractères spéciaux
      shot = shot.encode()
      # On envoie le message
      connexion_avec_serveur.send(shot)
    elif signal== b"ok1": #coup valide J1
      gridsC[0].play(J1,int(shot))
      gridsC[0].display()
    elif signal == b"ok2": #coup valide J2
      gridsC[1].play(J2,int(shot))
      gridsC[1].display()
  if signal == b"w1":
    print("Joueur1 vous avez gagné!")
  elif signal == b"l1":
    prinf("Joueur1 vous avez perdu!")
  elif signal == b"w2":
    prinf("Joueur2 vous avez gagné!")
  elif signal == b"l2":
    prinf("Joueur2 vous avez perdu!")
  elif signal == b"draw":
    print("Match NUL !")

  print("Fermeture de la connexion")
  connexion_avec_serveur.close()


def initialisationClient():
  print('###Mise en réseau - Client')
  try:
    if len(sys.argv) != 2:
      print("Erreur : nombre d'arguments invalide")
    else:
      h=socket.gethostbyname(sys.argv[1])
      print(h)
      p = int (input("Entrez le numéro de port svp (voir port serveur): \n"))
  except TypeError:
    print("Type incompatible")
  except NameError:
    print("### ERREUR -> Saisie invalide, veuillez relancer une demande de serveur")
  else:
    #on suppose que le hostname est entré correctement
    port=p

    connexion(p,h)

initialisationClient();
