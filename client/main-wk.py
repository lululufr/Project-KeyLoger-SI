from env import *

import argparse
import socket
def argument():
    p = argparse.ArgumentParser(description='Ajouter description')
    p.add_argument('-p', '--ping', action='store_true', help='Fais un scan via Ping, pour voir les machines UP')
    p.add_argument('-s', '--socket',type=all, help="Recherche si le port spécifié est UP, mettre autre chose qu'un INT pour faire sur les 100 premiers ports")
    p.add_argument('-o', action='store_true', help='Enregistre les resultats dans un fichier')
    args = p.parse_args()
    return args



####connection avec le serveur

## Thread 1
# activation du script
# Lancement d'une requette au srv

# toutes les X frappes de clavier - Refresh renvoi au srv

##Thread 2
# Ecouter serveur


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect((SRV, PORT))

message = "TEST TEST TEST , Lucas est stylé"
client_socket.send(message.encode('utf-8')) ##envoi

# Recevoir des données du serveur
response = client_socket.recv(1024) ### 124 taille du message en octet
print(f"Réponse du serveur : {response.decode('utf-8')}")


# Fermer la connexion
client_socket.close()



