from grid import *
import socket
import select
hote = ''
port = 12800 #valeur par défaut

def connexion():
  connexion_principale = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  connexion_principale.bind((hote, port))
  connexion_principale.listen(5)
  print("Le serveur écoute à présent sur le port {}".format(port))
  return True

def initialisationServeur():
  print("## Mise en réseau - Serveur")
	hote = '192.168.42.11'
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
		PORT = p
		res= connexion()
		print("Serveur initialisé avec succès.")
		return True

serveur_lance = initialisationServeur()
partie_lance = False
clients_connectes = []
current_player = J1

while serveur_lance:
    # On vérifie que de nouveaux clients ne demandent pas à se connecter
    connexions_demandees, wlist, xlist = select.select([connexion_principale],
            [], [], 0.05)
        
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
        if current_player == J1: #Si c'est le tour de J1
            CJ1.send(b"yourshot")
            signal = CJ1.recv(1024)
            signal = signal.decode()
            print(signal)
                
                
        else : #Si c'est le tour de J2
            CJ2.send(b"yourshot")
            signal = CJ2.recv(1024)
            signal = signal.decode()
            print(signal)
                
        current_player = current_player%2+1

print("Fermeture des connexions")
for client in clients_connectes:
    client.close()
connexion_principale.close()

