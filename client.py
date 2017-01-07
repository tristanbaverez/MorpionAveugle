# -*-coding:utf-8 -*
from grid import *
import socket
import select
import sys

hote = "" #vide par défault

def connexion(port, hote):
  connexion_avec_serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  connexion_avec_serveur.connect((hote, port))
  print("#Connexion établie avec le serveur sur le port {}".format(port))

  grille =grid() #grille selon le joueur qu'on est
  shot = ""
  while (shot != "fin") or (signal != b"w1") or (signal != b"w2") or (signal != b"l1") or (signal != b"l2") or (signal != b"draw"):
    signal = connexion_avec_serveur.recv(1024)
    signal = signal.decode()
    if (signal == b"yourshot") or (signal == b"deb"): 
      if signal == b"deb":
        print("C'est à vous de commencer")     
      print("#Entrez le coup souhaité (attention mettre des guillemets)\n (valeur entre 0 et 8)\n")
      shot =input("> ")
      # Peut planter si vous tapez des caractères spéciaux
      shot = shot.encode()
      # On envoie le message
      connexion_avec_serveur.send(shot)
    elif signal== b"ok1": #coup valide J1
      grille.play(J1,int(shot)) #rajoute un rond
      grille.display()
      print("En attente du J2...")
    elif signal == b"ok2": #coup valide J2
      grille.play(J2,int(shot)) #rajoute une croix
      grille.display()
      print("En attente du J1...")
    elif signal == b"occupe":# prédicat afin d'inviter le joueur à rejouer en cas de case entrée occupée
        print("Case occupée, Rejouez svp")  
    elif signal == b"w1":
      print("##Joueur1 vous avez gagné!")
    elif signal == b"l1":
      print("##Joueur1 vous avez perdu!")
    elif signal == b"w2":
      print("##Joueur2 vous avez gagné!")
    elif signal == b"l2":
      print("##Joueur2 vous avez perdu!")
    elif signal == b"draw":
      print("##Match NUL !")
    #tests pour les spectateurs 
    elif signal == b"debSpec":
      print("\n##Mode spectateur")
    elif signal == b"end1":
      print("Joueur1 a gagné")
    elif signal == b"end2":
      print("Joueur2 a gagné")
    elif int(signal) < 20 :
      grille.play(J1,int(signal)-10)
      grille.display()
      print("J1 -> "+str(int(signal)-10))
    elif int(signal) >= 20:
      grille.play(J2,int(signal)-20)
      grille.display()
      print("J2 -> "+str(int(signal)-20))
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
