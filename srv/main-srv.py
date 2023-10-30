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

server_socket.listen(5) # 5 co en attente max

print("Le serveur attend une connexion...")
client_socket, addr = server_socket.accept()
print(f"Connexion établie avec {addr}")

# Réception du nom du fichier
filename = client_socket.recv(1024).decode('utf-8')
print(f"Nom du fichier reçu : {filename}")

# Ouvrir le fichier en mode binaire pour écriture
with open(filename, 'wb') as file:
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        file.write(data)

print(f"Le fichier '{filename}' a été reçu avec succès.")

# Fermez la connexion et le socket
client_socket.close()
server_socket.close()

