import argparse
import socket
from env import *


def argument():
    p = argparse.ArgumentParser(description='NMAP MAIS EN MIEUX en faite.')
    p.add_argument('-p', '--ping', action='store_true', help='Fais un scan via Ping, pour voir les machines UP')
    p.add_argument('-s', '--socket',type=all, help="Recherche si le port spécifié est UP, mettre autre chose qu'un INT pour faire sur les 100 premiers ports")
    p.add_argument('-o', action='store_true', help='Enregistre les resultats dans un fichier')
    args = p.parse_args()
    return args



server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind(("0.0.0.0", PORT))

# Écoute pour les connexions entrantes (maximum 5 connexions en attente)

while True :
    server_socket.listen(5)

    print(f"Le serveur écoute sur {SRV}:{PORT}")

    # Attente d'une connexion entrante
    client_socket, client_address = server_socket.accept()
    print(f"Connexion acceptée de {client_address}")

    # Recevoir des données du client
    data = client_socket.recv(1024)
    print(f"Données reçues du client : {data.decode('utf-8')}")

    # Envoyer des données au client
    response = "Bonjour, client !"
    client_socket.send(response.encode('utf-8'))

# Fermer les connexions
client_socket.close()
server_socket.close()

