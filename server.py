# -*-coding:utf-8 -*

from grid import *
import socket
import select
import random

hote = ""

def connexion(port):
  connexion_principale = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  connexion_principale.bind((hote, port))
  connexion_principale.listen(5)
  print("Le serveur écoute à présent sur le port {}".format(port))
  
  serveur_lance = True
  partie_lance = False
  clients_connectes = []
  current_player = random.randint(1,2)#on choisit arbitrairement qui va débuter la partie

  while serveur_lance:
    # On vérifie que de nouveaux clients ne demandent pas à se connecter
    connexions_demandees, wlist, xlist = select.select([connexion_principale],[], [], 0.05)

    for connexion in connexions_demandees:
      connexion_avec_client, infos_connexion = connexion.accept()
      # On ajoute le socket connecté à la liste des clients
      clients_connectes.append(connexion_avec_client)

      #Les deux premiers clients sont les joueurs 1 et 2
    if len(clients_connectes)>=2 and not(partie_lance):
      CJ1 = clients_connectes[0]
      CJ2 = clients_connectes[1]
      partie_lance = True

    if partie_lance :
      #initialisation de la grille dans la partie serveur
      grids = [grid(), grid(), grid()]  
      occupe =False 
      debut=True
      while grids[0].gameOver() == -1: #tant que la partie n'est pas terminée
        if not(occupe) and not(debut):# ici on test si il y'a eu un coup occupé pour l'attribution du tour de jeu
          current_player = current_player%2+1
        else:
          occupe=False
        shot= -1
        if current_player == J1: #Si c'est le tour de J1 
          if debut:
            CJ1.send(b"deb")
          else:      
            CJ1.send(b"yourshot")
          signal = CJ1.recv(1024)
          signal = signal.decode()
          print(signal)
          shot= int(signal)
          while shot <0 or shot >=NB_CELLS:
            CJ1.send(b"yourshot")
            signal = CJ1.recv(1024)
            signal = signal.decode()
            print(signal)
            shot= int(signal)
        else :#Si c'est le tour de J2
          if debut:
            CJ2.send(b"deb")
          else:    
            CJ2.send(b"yourshot")
          signal = CJ2.recv(1024)
          signal = signal.decode()
          print(signal)
          shot= int(signal)
          while shot <0 or shot >=NB_CELLS:
            CJ2.send(b"yourshot")
            signal = CJ2.recv(1024)
            signal = signal.decode()
            print(signal)
            shot= int(signal)     
        if (grids[0].cells[shot] != EMPTY):
          grids[current_player].cells[shot] = grids[0].cells[shot]
          if current_player==J1:
            CJ1.send(b"occupe")
          elif current_player==J2:
            CJ2.send(b"occupe")
          occupe=True #booléen afin de ne pas changer de joueur au début de la boucle
        else: # cas où la case entrée par le joueur est valide
          grids[current_player].cells[shot] = current_player
          grids[0].play(current_player, shot)
          #on est obligé de renvoyer la validité ici afin que le client ne valide pas si la case est occupée
          if current_player==J1:
            CJ1.send(b"ok1")
          elif current_player==J2:
            CJ2.send(b"ok2")          
        grids[0].display()
        debut=False
      if grids[0].gameOver() == J1:
        print("J1 win !")
        CJ1.send(b"w1")         
        CJ2.send(b"l2")
      elif grids[0].gameOver() == J2:
        print("J2 win !")
        CJ1.send(b"l1")
        CJ2.send(b"w2")
      elif grids[0].gameOver == EMPTY:# cas d'égalité
        print("MATCH NUL")
        CJ1.send(b"draw")
        CJ2.send(b"draw")
  print("Fermeture des connexions, GAME OVER")
  for client in clients_connectes:
    client.close()
  connexion_principale.close()
 


def initialisationServeur():
  print("## Mise en réseau - Serveur")
  try:
    p = input("#Choix du port : (valeur entre 49152 et 65535\n")
    p = int(p)
    if (p < 49152) or (p > 65535):
      raise ValueError("Attention, domaine de port incorrect")
  except ValueError:
    print("Respecter l'ensemble de valeur svp")
  except TypeError:
    print("Type incompatible")
  except NameError:
    print("### ERREUR -> Saisie invalide, veuillez relancer une demande de serveur")
  else: #Si on arrive là tous les paramètres ont été saisie correctement
    port=p
    print("Serveur initialisé avec succès.")
    print("Hostname -> ", socket.gethostname())
    res= connexion(port)   

initialisationServeur()
